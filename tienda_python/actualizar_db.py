import sqlite3

DB_PATH = "tienda.db"

# Conectar a la base de datos
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === EJEMPLOS DE OPERACIONES ===

# 1️⃣ Insertar un nuevo producto
cursor.execute("""
INSERT INTO productos (nombre, precio, imagen_url)
VALUES (?, ?, ?)
""", ("Tomate cherry", 150, "img/tomate.jpg"))

# 2️⃣ Actualizar un producto existente (por id)
cursor.execute("""
UPDATE productos
SET precio = ?
WHERE id = ?
""", (200, 1))

# 3️⃣ Eliminar un producto (por id)
# cursor.execute("DELETE FROM productos WHERE id = ?", (3,))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("✅ Base de datos actualizada")
