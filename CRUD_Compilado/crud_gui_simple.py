#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRUD TIENDA - Conexión a MySQL (Versión Simplificada)
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error

# CONFIG MYSQL
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'tienda')
try:
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
except ValueError:
    MYSQL_PORT = 3306

# ======================== DATABASE ========================

def get_db_connection():
    """Conecta a la base de datos MySQL"""
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
        return None

def get_productos():
    """Obtiene productos de la base de datos MySQL"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, descripcion, precio, imagen_url as imagen, stock FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        return productos
    except Error as e:
        return []
    finally:
        conn.close()

def agregar_producto(nombre, descripcion, precio, imagen, stock):
    """Agrega un nuevo producto a la base de datos"""
    if not nombre:
        messagebox.showwarning("Validación", "El nombre es obligatorio")
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        query = "INSERT INTO productos (nombre, descripcion, precio, imagen_url, stock) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nombre, descripcion, precio, imagen, stock))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error agregando producto: {e}")
        return False
    finally:
        conn.close()

def actualizar_producto(id_prod, nombre, descripcion, precio, imagen, stock):
    """Actualiza un producto en la base de datos"""
    if not nombre:
        messagebox.showwarning("Validación", "El nombre es obligatorio")
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        query = "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, imagen_url=%s, stock=%s WHERE id=%s"
        cursor.execute(query, (nombre, descripcion, precio, imagen, stock, id_prod))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Éxito", "Producto actualizado correctamente")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error actualizando producto: {e}")
        return False
    finally:
        conn.close()

def eliminar_producto(id_prod):
    """Elimina un producto de la base de datos"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id=%s", (id_prod,))
        conn.commit()
        cursor.close()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error eliminando producto: {e}")
        return False
    finally:
        conn.close()

# ======================== GUI ========================

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Productos - Tienda (MySQL)")
        self.root.geometry("900x600")
        self.selected_id = None
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestión de Productos (MySQL)", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Estado de conexión
        self.status_label = ttk.Label(main_frame, text="", foreground="green")
        self.status_label.grid(row=0, column=2, padx=10)
        self.check_connection()
        
        # ---- FORMULARIO ----
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Producto", padding="10")
        form_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=10, pady=10)
        
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
        ttk.Button(button_frame, text="Recargar", command=self.refresh_tabla).pack(side=tk.LEFT, padx=5)
        
        # ---- TABLA ----
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Productos (MySQL)", padding="10")
        table_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Columnas
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
    
    def check_connection(self):
        """Comprueba si hay conexión a MySQL"""
        conn = get_db_connection()
        if conn:
            self.status_label.config(text="✓ Conectado a MySQL", foreground="green")
            conn.close()
        else:
            self.status_label.config(text="✗ No hay conexión", foreground="red")
    
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
    
    def eliminar(self):
        """Elimina el producto seleccionado"""
        if not self.selected_id:
            messagebox.showwarning("Selección", "Selecciona un producto para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este producto?"):
            if eliminar_producto(self.selected_id):
                self.refresh_tabla()
                self.limpiar_form()
    
    def on_select(self, event):
        """Carga los datos del producto seleccionado"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, 'values')
            id_prod = int(values[0])
            
            productos = get_productos()
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
        """Refresca la tabla de productos desde MySQL"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar productos desde la base de datos
        productos = get_productos()
        if not productos:
            messagebox.showwarning("Información", "No se encontraron productos en la BD o hay error de conexión")
            return
        
        for p in productos:
            try:
                self.tree.insert('', 0, values=(
                    p['id'],
                    p['nombre'],
                    p['descripcion'][:50] if p['descripcion'] else "",
                    f"${p['precio']:.2f}",
                    p['stock']
                ))
            except Exception as e:
                print(f"Error insertando producto {p.get('id')}: {e}")

# ======================== MAIN ========================

if __name__ == '__main__':
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
