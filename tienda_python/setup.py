#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup para compilar crud_gui.py a CRUD.exe usando py2exe
"""

from distutils.core import setup
import py2exe
import sys
import os

# Configuración de py2exe
options = {
    "py2exe": {
        "includes": ["tkinter", "mysql.connector", "re"],
        "packages": [],
        "dist_dir": os.path.join(os.path.dirname(__file__), '..', 'CRUD_Compilado'),
        "bundle_files": 1,
        "optimize": 2,
    }
}

setup(
    name='CRUD Tienda',
    version='1.0',
    description='Aplicación de gestión de productos para tienda',
    author='Desarrollo',
    script_args=['py2exe'],
    options=options,
    console=[{
        'script': 'crud_gui.py',
        'dest_base': 'CRUD'
    }],
    zipfile=None,
)
