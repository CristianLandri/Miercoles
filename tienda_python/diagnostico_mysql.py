#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico completo de conexión MySQL
"""
import os
import sys
import mysql.connector
from mysql.connector import Error

print("=== DIAGNÓSTICO MYSQL ===\n")

# 1. Verificar variables de entorno
print("1. Variables de entorno:")
print(f"   MYSQL_HOST: {os.getenv('MYSQL_HOST', 'NO DEFINIDA (usando localhost)')}")
print(f"   MYSQL_USER: {os.getenv('MYSQL_USER', 'NO DEFINIDA (usando root)')}")
print(f"   MYSQL_PASSWORD: {os.getenv('MYSQL_PASSWORD', 'NO DEFINIDA (vacía)')}")
print(f"   MYSQL_DATABASE: {os.getenv('MYSQL_DATABASE', 'NO DEFINIDA (usando tienda)')}")
print(f"   MYSQL_PORT: {os.getenv('MYSQL_PORT', 'NO DEFINIDA (usando 3306)')}\n")

# 2. Intentar conectar
config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'port': int(os.getenv('MYSQL_PORT', '3306'))
}

print("2. Intentando conectar al servidor MySQL...")
try:
    conn = mysql.connector.connect(**config)
    print("   ✓ Conexión al servidor OK\n")
except Error as e:
    print(f"   ✗ ERROR: {e}\n")
    sys.exit(1)

# 3. Listar bases de datos
print("3. Bases de datos disponibles:")
try:
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    dbs = [row[0] for row in cursor.fetchall()]
    for db in dbs:
        print(f"   - {db}")
    print()
except Error as e:
    print(f"   ✗ ERROR: {e}\n")
    sys.exit(1)

# 4. Conectar a la base 'tienda'
db_name = os.getenv('MYSQL_DATABASE', 'tienda')
print(f"4. Intentando conectar a la base '{db_name}'...")
try:
    cursor.execute(f"USE {db_name}")
    print(f"   ✓ Conectado a '{db_name}'\n")
except Error as e:
    print(f"   ✗ ERROR: {e}")
    print(f"   → La base '{db_name}' NO existe o no es accesible\n")
    conn.close()
    sys.exit(1)

# 5. Listar tablas
print("5. Tablas en la base de datos:")
try:
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    if tables:
        for tbl in tables:
            print(f"   - {tbl}")
    else:
        print("   ✗ NO hay tablas\n")
    print()
except Error as e:
    print(f"   ✗ ERROR: {e}\n")
    sys.exit(1)

# 6. Inspeccionar tabla 'productos'
print("6. Tabla 'productos':")
if 'productos' in tables:
    try:
        cursor.execute("DESCRIBE productos")
        columns = cursor.fetchall()
        print("   Columnas:")
        for col in columns:
            print(f"      {col[0]} ({col[1]})")
        print()
        cursor.execute("SELECT COUNT(*) FROM productos")
        count = cursor.fetchone()[0]
        print(f"   ✓ Registros: {count}\n")
    except Error as e:
        print(f"   ✗ ERROR: {e}\n")
else:
    print("   ✗ La tabla 'productos' NO existe\n")
    print("   → Necesitas crear la tabla. Aquí está el SQL:\n")
    print("""
    CREATE TABLE productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        descripcion TEXT,
        precio DECIMAL(10, 2),
        imagen VARCHAR(255),
        stock INT DEFAULT 0
    );
    """)

cursor.close()
conn.close()
print("=== FIN DIAGNÓSTICO ===")
