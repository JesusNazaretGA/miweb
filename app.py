from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def crear_tabla_si_no_existe():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def guardar_usuario(correo, password):
    hashed_password = generate_password_hash(password)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (correo, password) VALUES (%s, %s)', (correo, hashed_password))
        conn.commit()
        return True, "Usuario registrado exitosamente."
    except psycopg2.IntegrityError:
        conn.rollback()
        return False, "Este correo ya está registrado."
    finally:
        cursor.close()
        conn.close()

def verificar_usuario(correo, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM usuarios WHERE correo = %s', (correo,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row and check_password_hash(row[0], password):
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = None
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        if not correo or not password:
            mensaje = "Por favor, completa todos los campos."
        else:
            # Intentamos verificar si usuario existe y contraseña es correcta
            if verificar_usuario(correo, password):
                return render_template('exito.html', correo=correo)
            else:
                # Si no existe, intentamos registrarlo
                exito, mensaje = guardar_usuario(correo, password)
    return render_template('login.html', mensaje=mensaje)

if __name__ == "__main__":
    crear_tabla_si_no_existe()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
