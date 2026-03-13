import sqlite3

conexion = sqlite3.connect("pedidos.db")

cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    platillo TEXT,
    cantidad INTEGER,
    estado TEXT, 
    tiempo_estimado INTEGER
)
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")