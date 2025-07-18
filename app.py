from flask import Flask, render_template, request
import os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

def crear_tabla_si_no_existe():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                correo TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creando tabla: {e}")

def registrar_usuario(correo, password):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (correo, password) VALUES (%s, %s)', (correo, password))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Usuario registrado exitosamente."
    except psycopg2.errors.UniqueViolation:
        return False, "Este correo ya está registrado."
    except Exception as e:
        return False, f"Error al guardar usuario: {e}"

def verificar_usuario(correo, password):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM usuarios WHERE correo = %s', (correo,))
        fila = cursor.fetchone()
        cursor.close()
        conn.close()
        if fila and fila[0] == password:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al verificar usuario: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = None
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        accion = request.form.get('accion')  # para diferenciar registro/login

        if not correo or not password:
            mensaje = "Por favor, completa todos los campos."
        else:
            if accion == "registrar":
                exito, mensaje = registrar_usuario(correo, password)
            elif accion == "login":
                if verificar_usuario(correo, password):
                    return f"<h2>¡Bienvenido {correo}!</h2><p>Has iniciado sesión correctamente.</p>"
                else:
                    mensaje = "Correo o contraseña incorrectos."

    return render_template('login.html', mensaje=mensaje)

@app.route('/usuarios')
def listar_usuarios():
    usuarios = []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT id, correo, password FROM usuarios')
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        return f"Error al consultar la base de datos: {e}"

    html = "<h1>Usuarios registrados</h1><ul>"
    for u in usuarios:
        html += f"<li>ID: {u[0]} - Correo: {u[1]} - Contraseña: {u[2]}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    crear_tabla_si_no_existe()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
