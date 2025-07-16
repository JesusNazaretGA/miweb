import sqlite3

# Conectamos a la base de datos (se crea si no existe)
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Creamos la tabla usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        correo TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insertamos un usuario de prueba
cursor.execute('''
    INSERT OR IGNORE INTO usuarios (correo, password)
    VALUES (?, ?)
''', ('prueba@correo.com', '123456'))

conn.commit()
conn.close()
print("Base de datos creada con usuario prueba@correo.com / 123456")
