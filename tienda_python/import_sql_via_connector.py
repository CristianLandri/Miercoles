#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from mysql.connector import connect, Error

SQL_PATH = os.path.join(os.path.dirname(__file__), 'Nueva carpeta', 'tienda (1).sql')

if not os.path.exists(SQL_PATH):
    print('ERROR: no se encontró el archivo SQL en', SQL_PATH)
    sys.exit(2)

import re

with open(SQL_PATH, 'r', encoding='utf-8', errors='ignore') as f:
    sql = f.read()

try:
    conn = connect(host='localhost', user='root', password='', port=3306)
    cursor = conn.cursor()
    # Split simple statements by semicolon followed by newline (not perfect for complex dumps)
    statements = [s.strip() for s in re.split(r";\s*\n", sql) if s.strip()]
    for stmt in statements:
        try:
            cursor.execute(stmt)
        except Error as e:
            # Mostrar pero seguir con el resto de sentencias
            print('Warning executing statement:', e)
    conn.commit()
    print('Import OK')
except Error as e:
    print('ERROR:', e)
    sys.exit(1)
finally:
    try:
        cursor.close()
    except Exception:
        pass
    try:
        conn.close()
    except Exception:
        pass
