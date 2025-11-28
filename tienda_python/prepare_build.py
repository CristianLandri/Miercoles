#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup para compilar crud_gui.py a CRUD.exe usando py2exe
Ejecutar desde el directorio de tienda_python
"""

from distutils.core import setup
import py2exe
import sys
import os
import shutil

# Crear setup.py en la carpeta temporal
setup_content = '''from distutils.core import setup
import py2exe

setup(
    name='CRUD Tienda',
    version='1.0',
    description='Aplicación de gestión de productos para tienda',
    console=[{'script': 'crud_gui.py', 'dest_base': 'CRUD'}],
    options={
        'py2exe': {
            'includes': ['tkinter', 'mysql.connector', 're'],
            'bundle_files': 1,
            'optimize': 2,
            'dist_dir': 'dist',
        }
    },
    zipfile=None,
)
'''

# Copiar archivos necesarios
tienda_path = os.path.dirname(os.path.abspath(__file__))
crud_source = os.path.join(tienda_path, 'crud_gui.py')

if os.path.exists(crud_source):
    # Crear archivo setup.py temporal
    setup_file = os.path.join(tienda_path, 'setup_build.py')
    with open(setup_file, 'w', encoding='utf-8') as f:
        f.write(setup_content)
    
    print("✓ Archivos preparados para compilación")
    print(f"  Ubicación: {tienda_path}")
else:
    print("✗ No se encontró crud_gui.py")
