#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para subir CRUD.exe a una base de datos SQLite local (builds.sqlite)
Guarda (filename, data BLOB, file_size, created_at).
"""
import os
import sys
import sqlite3
from datetime import datetime

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXE_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'CRUD_Compilado', 'CRUD.exe'))
DB_PATH = os.path.join(BASE_DIR, 'builds.sqlite')

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS builds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    data BLOB NOT NULL,
    file_size INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
'''

INSERT_SQL = 'INSERT INTO builds (filename, data, file_size, created_at) VALUES (?, ?, ?, ?)'


def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(CREATE_TABLE_SQL)
    conn.commit()
    cur.close()
    conn.close()


def upload_file():
    if not os.path.exists(EXE_PATH):
        print(f"ERROR: no se encontró el ejecutable en: {EXE_PATH}")
        return 2

    with open(EXE_PATH, 'rb') as f:
        blob = f.read()

    fname = os.path.basename(EXE_PATH)
    size = len(blob)
    created_at = datetime.now().isoformat(sep=' ', timespec='seconds')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(INSERT_SQL, (fname, blob, size, created_at))
    conn.commit()
    last_id = cur.lastrowid
    cur.close()
    conn.close()

    print(f"Éxito: archivo '{fname}' subido a '{DB_PATH}' con id={last_id}, {size} bytes")
    return 0


def main():
    ensure_db()
    return upload_file()

if __name__ == '__main__':
    sys.exit(main())
