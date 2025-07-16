from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
import sqlite3
import os

app = Flask(__name__)

def crear_tabla_si_no_existe():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def guardar_usuario(correo, password):
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (correo, password) VALUES (?, ?)', (correo, hashed_password))
        conn.commit()
        return True, "Usuario registrado exitosamente."
    except sqlite3.IntegrityError:
        return False, "Este correo ya está registrado."
    finally:
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = None
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        if not correo or not password:
            mensaje = "Por favor, completa todos los campos."
        else:
            exito, mensaje = guardar_usuario(correo, password)
    return render_template('login.html', mensaje=mensaje)

if __name__ == "__main__":
    crear_tabla_si_no_existe()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=10000, debug=True)
