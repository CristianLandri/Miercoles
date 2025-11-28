#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para subir CRUD.exe a la base de datos MySQL.
Se crea la tabla `builds` si no existe y se inserta el binario.
Ajusta las credenciales en la sección CONFIG si es necesario.
"""
import os
import sys
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# === CONFIG ===
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'tienda'
MYSQL_PORT = 3306

EXE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'CRUD_Compilado', 'CRUD.exe'))


def create_table_if_not_exists(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS builds (
        id INT AUTO_INCREMENT PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        data LONGBLOB NOT NULL,
        file_size BIGINT NOT NULL,
        created_at DATETIME NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    conn.commit()
    cur.close()


def upload_file(conn, filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    fname = os.path.basename(filepath)
    size = len(data)
    cur = conn.cursor()
    sql = "INSERT INTO builds (filename, data, file_size, created_at) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (fname, data, size, datetime.now()))
    conn.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id, size


def main():
    if not os.path.exists(EXE_PATH):
        print(f"ERROR: No se encontró el ejecutable en: {EXE_PATH}")
        sys.exit(2)

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        create_table_if_not_exists(conn)
        inserted_id, size = upload_file(conn, EXE_PATH)
        print(f"Éxito: archivo '{os.path.basename(EXE_PATH)}' subido con id={inserted_id}, {size} bytes")
        conn.close()
    except Error as e:
        print(f"ERROR BD: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
