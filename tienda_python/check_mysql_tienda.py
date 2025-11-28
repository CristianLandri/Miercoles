#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación: conecta a MySQL y muestra información básica
"""
import mysql.connector
from mysql.connector import Error

import os

config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'port': int(os.getenv('MYSQL_PORT', '3306')),
    'database': os.getenv('MYSQL_DATABASE', 'tienda')
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('SHOW DATABASES')
    dbs = [row[0] for row in cursor.fetchall()]
    print('Databases:', dbs)
    if 'tienda' in dbs:
        cursor.execute('USE tienda')
        cursor.execute('SHOW TABLES')
        tables = [row[0] for row in cursor.fetchall()]
        print('Tables in tienda:', tables)
        if 'productos' in tables:
            cursor.execute('SELECT COUNT(*) FROM productos')
            cnt = cursor.fetchone()[0]
            print('productos rows:', cnt)
    else:
        print("Database 'tienda' not found")
    cursor.close()
    conn.close()
except Error as e:
    print('ERROR connecting to MySQL:', e)
    raise
