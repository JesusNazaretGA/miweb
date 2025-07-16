from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def crear_tabla_si_no_existe():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def guardar_usuario(correo, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (correo, password) VALUES (?, ?)', (correo, password))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = None
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        guardar_usuario(correo, password)
        mensaje = f'Se guardó el correo {correo} con su contraseña.'
    return render_template('login.html', mensaje=mensaje)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render asigna el puerto por variable de entorno
    app.run(host="0.0.0.0", port=port, debug=True)

