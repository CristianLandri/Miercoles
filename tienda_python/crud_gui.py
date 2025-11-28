#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUD TIENDA - Aplicación de Escritorio GUI con tkinter
Windows 32-bit compatible Python application
Gestión de productos: nombre, descripcion, precio, imagen, stock
Conectado a base de datos MySQL y Tienda.html
"""

import sys
import os
import re
import logging
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ======================== CONFIG (env) ========================
# Logging for DB connection issues
LOG_PATH = os.path.join(os.path.dirname(__file__), 'crud_gui_connection.log')
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Read MySQL connection settings from environment variables (fallback to defaults)
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'tienda')
try:
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
except ValueError:
    MYSQL_PORT = 3306

TIENDA_HTML_PATH = os.path.join(os.path.dirname(__file__), '..', 'Tienda.html')

# ======================== DATABASE ========================

def get_db_connection():
    """Conecta a base de datos MySQL"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        return conn
    except Error as e:
        # Mostrar y loguear error de conexión
        try:
            messagebox.showerror("Error BD", f"Error de conexión: {e}")
        except Exception:
            pass
        logging.error('DB connection error: %s', e)
        return None

def init_database():
    """Inicializa la base de datos y tabla si no existen"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        cursor = conn.cursor()
        
        # Crear BD si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
        cursor.execute(f"USE {MYSQL_DATABASE}")
        
        # Crear tabla productos con imagen_url (nombre correcto de BD)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                descripcion TEXT,
                precio DECIMAL(10, 2),
                imagen_url VARCHAR(255),
                stock INT DEFAULT 0
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Base de datos inicializada correctamente")
    except Error as e:
        print(f"✗ Error inicializando BD: {e}")

def obtener_productos():
    """Obtiene todos los productos de la BD"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Usar imagen_url directamente - es el nombre correcto de la columna
        query = "SELECT id, nombre, descripcion, precio, imagen_url as imagen, stock FROM productos"
        cursor.execute(query)
        productos = cursor.fetchall()
        cursor.close()
        return productos
    except Error as e:
        try:
            messagebox.showerror("Error", f"Error obteniendo productos: {e}")
        except:
            pass
        return []
    finally:
        conn.close()

def agregar_producto(nombre, descripcion, precio, imagen, stock):
    """Agrega un nuevo producto a la BD"""
    if not nombre:
        messagebox.showwarning("Validación", "El nombre es obligatorio")
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        # Usar imagen_url directamente
        query = """
            INSERT INTO productos (nombre, descripcion, precio, imagen_url, stock)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre, descripcion, precio, imagen, stock))
        conn.commit()
        cursor.close()
        try:
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
        except:
            pass
        return True
    except Error as e:
        try:
            messagebox.showerror("Error", f"Error agregando producto: {e}")
        except:
            pass
        return False
    finally:
        conn.close()

def actualizar_producto(id_prod, nombre, descripcion, precio, imagen, stock):
    """Actualiza un producto existente"""
    if not nombre:
        messagebox.showwarning("Validación", "El nombre es obligatorio")
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        # Usar imagen_url directamente
        query = """
            UPDATE productos 
            SET nombre=%s, descripcion=%s, precio=%s, imagen_url=%s, stock=%s
            WHERE id=%s
        """
        cursor.execute(query, (nombre, descripcion, precio, imagen, stock, id_prod))
        conn.commit()
        cursor.close()
        try:
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
        except:
            pass
        return True
    except Error as e:
        try:
            messagebox.showerror("Error", f"Error actualizando producto: {e}")
        except:
            pass
        return False
    finally:
        conn.close()

def eliminar_producto(id_prod):
    """Elimina un producto"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id=%s", (id_prod,))
        conn.commit()
        cursor.close()
        try:
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        except:
            pass
        return True
    except Error as e:
        try:
            messagebox.showerror("Error", f"Error eliminando producto: {e}")
        except:
            pass
        return False
    finally:
        conn.close()

def actualizar_tienda_html():
    """Actualiza Tienda.html con productos de la BD"""
    try:
        if not os.path.exists(TIENDA_HTML_PATH):
            print(f"⚠ Archivo no encontrado: {TIENDA_HTML_PATH}")
            return False
        
        productos = obtener_productos()
        
        # Generar HTML de productos
        html_items = ""
        for p in productos:
            img_path = p['imagen'] if p['imagen'] else "img/placeholder.jpg"
            html_items += f"""            <div class="item">
                <figure>
                    <img src="{img_path}" alt="{p['nombre']}">
                </figure>
                <div class="info-item">
                    <h2>{p['nombre']}</h2>
                    <p class="price" style='font-weight:bold;'>${p['precio']:.2f}</p>
                    <p>{p['descripcion'] or ''}</p>
                    <p class='stock' style='font-size:12px;color:#666;'>Stock: {p['stock']}</p>
                    <button class='btn-add-cart' data-id='{p['id']}' {"" if p['stock'] > 0 else "disabled"}>Añadir al carrito</button>
                </div>
            </div>
            
"""
        
        # Leer archivo original
        with open(TIENDA_HTML_PATH, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Reemplazar el primer contenedor que tenga id="server-products" (más flexible)
        patron = r'(<div[^>]*id="server-products"[^>]*>)(.*?)(</div>)'
        contenido_nuevo = re.sub(
            patron,
            r'\1\n            <!-- SERVER_PRODUCTS -->\n' + html_items + r'\3',
            contenido,
            count=1,
            flags=re.DOTALL
        )
        # Medida defensiva: eliminar contenedores adicionales dejando sólo el primero
        # Buscar todos los contenedores y extraer el primero
        all_matches = re.findall(patron, contenido_nuevo, flags=re.DOTALL)
        if len(all_matches) > 1:
            # Mantener sólo el primero: reconstruir contenido removiendo los siguientes
            first = re.search(patron, contenido_nuevo, flags=re.DOTALL)
            if first:
                start, end = first.span()
                before = contenido_nuevo[:start]
                middle = contenido_nuevo[start:end]
                after = contenido_nuevo[end:]
                # Eliminar cualquier otro contenedor en 'after'
                after_clean = re.sub(patron, '', after, flags=re.DOTALL)
                contenido_nuevo = before + middle + after_clean
        
        # Guardar archivo actualizado
        with open(TIENDA_HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print("✓ Tienda.html actualizado")
        return True
    except Exception as e:
        print(f"✗ Error actualizando Tienda.html: {e}")
        return False

# ======================== GUI ========================

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Productos - Tienda")
        self.root.geometry("900x600")
        self.selected_id = None
        
        # Inicializar BD
        init_database()
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestión de Productos", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # ---- FORMULARIO ----
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Producto", padding="10")
        form_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.nombre_entry = ttk.Entry(form_frame, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W)
        self.desc_text = tk.Text(form_frame, width=30, height=3)
        self.desc_text.grid(row=1, column=1, padx=5, pady=5)
        
        # Precio
        ttk.Label(form_frame, text="Precio:").grid(row=2, column=0, sticky=tk.W)
        self.precio_entry = ttk.Entry(form_frame, width=30)
        self.precio_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Imagen
        ttk.Label(form_frame, text="Imagen (URL):").grid(row=3, column=0, sticky=tk.W)
        self.imagen_entry = ttk.Entry(form_frame, width=30)
        self.imagen_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Stock
        ttk.Label(form_frame, text="Stock:").grid(row=4, column=0, sticky=tk.W)
        self.stock_entry = ttk.Entry(form_frame, width=30)
        self.stock_entry.grid(row=4, column=1, padx=5, pady=5)
        self.stock_entry.insert(0, "0")
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Agregar", command=self.agregar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_form).pack(side=tk.LEFT, padx=5)
        
        # ---- TABLA ----
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Productos", padding="10")
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Columnas: ID, Nombre, Descripción, Precio, Stock
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Descripción", "Precio", "Stock"), height=12)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=40)
        self.tree.column("Nombre", anchor=tk.W, width=150)
        self.tree.column("Descripción", anchor=tk.W, width=250)
        self.tree.column("Precio", anchor=tk.W, width=80)
        self.tree.column("Stock", anchor=tk.W, width=60)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Nombre", text="Nombre", anchor=tk.W)
        self.tree.heading("Descripción", text="Descripción", anchor=tk.W)
        self.tree.heading("Precio", text="Precio", anchor=tk.W)
        self.tree.heading("Stock", text="Stock", anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Cargar datos
        self.refresh_tabla()
    
    def agregar(self):
        """Agrega un nuevo producto"""
        nombre = self.nombre_entry.get()
        descripcion = self.desc_text.get("1.0", tk.END).strip()
        try:
            precio = float(self.precio_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Validación", "Precio debe ser un número")
            return
        
        imagen = self.imagen_entry.get()
        try:
            stock = int(self.stock_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Validación", "Stock debe ser un número")
            return
        
        if agregar_producto(nombre, descripcion, precio, imagen, stock):
            self.refresh_tabla()
            self.limpiar_form()
            actualizar_tienda_html()
    
    def actualizar(self):
        """Actualiza el producto seleccionado"""
        if not self.selected_id:
            messagebox.showwarning("Selección", "Selecciona un producto para actualizar")
            return
        
        nombre = self.nombre_entry.get()
        descripcion = self.desc_text.get("1.0", tk.END).strip()
        try:
            precio = float(self.precio_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Validación", "Precio debe ser un número")
            return
        
        imagen = self.imagen_entry.get()
        try:
            stock = int(self.stock_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Validación", "Stock debe ser un número")
            return
        
        if actualizar_producto(self.selected_id, nombre, descripcion, precio, imagen, stock):
            self.refresh_tabla()
            self.limpiar_form()
            actualizar_tienda_html()
    
    def eliminar(self):
        """Elimina el producto seleccionado"""
        if not self.selected_id:
            messagebox.showwarning("Selección", "Selecciona un producto para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este producto?"):
            if eliminar_producto(self.selected_id):
                self.refresh_tabla()
                self.limpiar_form()
                actualizar_tienda_html()
    
    def on_select(self, event):
        """Carga los datos del producto seleccionado"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, 'values')
            id_prod = int(values[0])
            
            productos = obtener_productos()
            for p in productos:
                if p['id'] == id_prod:
                    self.selected_id = id_prod
                    self.nombre_entry.delete(0, tk.END)
                    self.nombre_entry.insert(0, p['nombre'])
                    
                    self.desc_text.delete("1.0", tk.END)
                    self.desc_text.insert("1.0", p['descripcion'] or "")
                    
                    self.precio_entry.delete(0, tk.END)
                    self.precio_entry.insert(0, str(p['precio']))
                    
                    self.imagen_entry.delete(0, tk.END)
                    self.imagen_entry.insert(0, p['imagen'] or "")
                    
                    self.stock_entry.delete(0, tk.END)
                    self.stock_entry.insert(0, str(p['stock']))
                    break
    
    def limpiar_form(self):
        """Limpia el formulario"""
        self.nombre_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.precio_entry.delete(0, tk.END)
        self.imagen_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, "0")
        self.selected_id = None
        self.tree.selection_remove(self.tree.selection())
    
    def refresh_tabla(self):
        """Refresca la tabla de productos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar productos
        productos = obtener_productos()
        for p in productos:
            self.tree.insert('', 0, values=(
                p['id'],
                p['nombre'],
                p['descripcion'][:50] if p['descripcion'] else "",
                f"${p['precio']:.2f}",
                p['stock']
            ))

# ======================== MAIN ========================

if __name__ == '__main__':
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
