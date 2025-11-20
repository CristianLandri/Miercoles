from http.server import SimpleHTTPRequestHandler, HTTPServer
import mysql.connector
from urllib.parse import parse_qs, urlparse
import os
import html as html_escape


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'tienda'
}

PORT = 8080


def obtener_productos():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos


def generar_html():
    productos = obtener_productos()
    items_html = ""

    for p in productos:
        stock = int(p.get('stock', 0) or 0)
        nombre = html_escape.escape(str(p.get('nombre', '')))
        precio = html_escape.escape(str(p.get('precio', '')))
        descripcion = html_escape.escape(str(p.get('descripcion') or ''))
        imagen = html_escape.escape(str(p.get('imagen_url', '')))
        idp = p.get('id')

        items_html += f"""
        <div class="item">
            <figure>
                <img src="{imagen}" alt="producto">
            </figure>
            <div class="info-product">
                <h2>{nombre}</h2>
                <p class="price">${precio}</p>
                <p>{descripcion}</p>
                <a href='/editar?id={idp}' class='btn-edit'>Editar</a>
                <a href='/eliminar?id={idp}' class='btn-delete'>Eliminar</a>
                <p class='stock'>Stock: {stock}</p>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tienda</title>
        <link rel="stylesheet" href="css/tienda.css">
    </head>
    <body>
        <header>
            <h1>AgroSt❀r Tienda☀</h1>
            <nav>
                <a href='/agregar' class='btn-add'>Agregar producto</a>
            </nav>
        </header>

        <div class="container-items">
            {items_html}
        </div>

        <script src="JF/index-1.js"></script>
    </body>
    </html>
    """
    return html


class TiendaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            contenido = generar_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(contenido)
        elif path == "/editar":
            params = parse_qs(parsed.query)
            id_producto = params.get("id", [None])[0]
            if id_producto:
                self.mostrar_formulario_edicion(id_producto)
            else:
                self.send_error(400, "ID de producto requerido")
        elif path == "/agregar":
            self.mostrar_formulario_agregar()
        elif path == "/eliminar":
            params = parse_qs(parsed.query)
            id_producto = params.get("id", [None])[0]
            if id_producto:
                self.mostrar_confirmacion_eliminar(id_producto)
            else:
                self.send_error(400, "ID de producto requerido")
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        longitud = int(self.headers.get('Content-Length', 0))
        datos = self.rfile.read(longitud).decode('utf-8')
        params = parse_qs(datos)

        if path == "/editar":
            id_producto = params.get("id", [None])[0]
            nombre = params.get("nombre", [None])[0]
            descripcion = params.get("descripcion", [None])[0]
            precio = params.get("precio", [None])[0]
            imagen_url = params.get("imagen_url", [None])[0]
            stock = params.get("stock", [None])[0]
            if id_producto and nombre and precio and imagen_url:
                self.actualizar_producto(id_producto, nombre, descripcion, precio, imagen_url, stock)
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_error(400, "Faltan datos para actualizar el producto")
        elif path == "/agregar":
            nombre = params.get("nombre", [None])[0]
            descripcion = params.get("descripcion", [None])[0]
            precio = params.get("precio", [None])[0]
            imagen_url = params.get("imagen_url", [None])[0]
            stock = params.get("stock", [0])[0]
            if nombre and precio and imagen_url:
                self.agregar_producto(nombre, descripcion, precio, imagen_url, stock)
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_error(400, "Faltan datos para agregar el producto")
        elif path == "/eliminar":
            id_producto = params.get("id", [None])[0]
            if id_producto:
                self.eliminar_producto(id_producto)
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_error(400, "ID de producto requerido")
        else:
            self.send_error(404, "Ruta POST no encontrada")

    def mostrar_formulario_edicion(self, id_producto):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
        producto = cursor.fetchone()
        conn.close()
        if not producto:
            self.send_error(404, "Producto no encontrado")
            return
        html = f"""
        <!DOCTYPE html>
        <html lang='es'>
        <head>
            <meta charset='UTF-8'>
            <title>Editar producto</title>
            <link rel='stylesheet' href='css/tienda.css'>
        </head>
        <body>
            <h1>Editar producto</h1>
            <form method='POST' action='/editar'>
                <input type='hidden' name='id' value='{producto['id']}'>
                <label>Nombre: <input name='nombre' value='{html_escape.escape(str(producto.get('nombre','')))}'></label><br>
                <label>Descripción: <textarea name='descripcion'>{html_escape.escape(str(producto.get('descripcion') or ''))}</textarea></label><br>
                <label>Precio: <input name='precio' type='number' step='0.01' value='{producto.get('precio','')}'></label><br>
                <label>Imagen URL: <input name='imagen_url' value='{html_escape.escape(str(producto.get('imagen_url','')))}'></label><br>
                <label>Stock: <input name='stock' type='number' value='{producto.get('stock',0)}'></label><br>
                <button type='submit'>Guardar</button>
            </form>
            <a href='/'>Volver a la tienda</a>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def mostrar_formulario_agregar(self):
        html = """
        <!DOCTYPE html>
        <html lang='es'>
        <head>
            <meta charset='UTF-8'>
            <title>Agregar producto</title>
            <link rel='stylesheet' href='css/tienda.css'>
        </head>
        <body>
            <h1>Agregar producto</h1>
            <form method='POST' action='/agregar'>
                <label>Nombre: <input name='nombre'></label><br>
                <label>Descripción: <textarea name='descripcion'></textarea></label><br>
                <label>Precio: <input name='precio' type='number' step='0.01'></label><br>
                <label>Imagen URL: <input name='imagen_url'></label><br>
                <label>Stock: <input name='stock' type='number' value='0'></label><br>
                <button type='submit'>Agregar</button>
            </form>
            <a href='/'>Volver a la tienda</a>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def mostrar_confirmacion_eliminar(self, id_producto):
        html = f"""
        <!DOCTYPE html>
        <html lang='es'>
        <head>
            <meta charset='UTF-8'>
            <title>Eliminar producto</title>
            <link rel='stylesheet' href='css/tienda.css'>
        </head>
        <body>
            <h1>Eliminar producto</h1>
            <p>¿Confirma que desea eliminar el producto ID {id_producto}?</p>
            <form method='POST' action='/eliminar'>
                <input type='hidden' name='id' value='{id_producto}'>
                <button type='submit'>Eliminar</button>
            </form>
            <a href='/'>Cancelar</a>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def actualizar_producto(self, id_producto, nombre, descripcion, precio, imagen_url, stock):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, imagen_url=%s, stock=%s WHERE id=%s",
            (nombre, descripcion, precio, imagen_url, stock or 0, id_producto)
        )
        conn.commit()
        conn.close()
        self.actualizar_html_estatico()

    def agregar_producto(self, nombre, descripcion, precio, imagen_url, stock):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, imagen_url, stock) VALUES (%s,%s,%s,%s,%s)",
            (nombre, descripcion, precio, imagen_url, stock or 0)
        )
        conn.commit()
        conn.close()
        self.actualizar_html_estatico()

    def eliminar_producto(self, id_producto):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
        conn.commit()
        conn.close()
        self.actualizar_html_estatico()

    def actualizar_html_estatico(self):
        productos = obtener_productos()
        items_html = ""
        # Generar HTML de items SOLO para Tienda.html (sin botones Editar/Eliminar, solo compra)
        for p in productos:
            stock = int(p.get('stock', 0) or 0)
            nombre = html_escape.escape(str(p.get('nombre', '')))
            precio = html_escape.escape(str(p.get('precio', '')))
            descripcion = html_escape.escape(str(p.get('descripcion') or ''))
            imagen = html_escape.escape(str(p.get('imagen_url', '')))
            idp = p.get('id')

            stock_status = f"Stock: {stock}" if stock > 0 else "Sin stock"

            items_html += f"""
            <div class='item'>
                <figure>
                    <img src='{imagen}' alt='producto'>
                </figure>
                <div class='info-product'>
                    <h2>{nombre}</h2>
                    <p class='price'>${precio}</p>
                    <p>{descripcion}</p>
                    {("<button class='btn-add-cart' disabled>Añadir al carrito</button>") if stock == 0 else ("<button class='btn-add-cart'>Añadir al carrito</button>")}
                    <p class='stock'>{stock_status}</p>
                </div>
            </div>
            """
        # Buscar Tienda.html en la carpeta padre del script
        ruta_html = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Tienda.html'))
        try:
            with open(ruta_html, 'r', encoding='utf-8') as f:
                html = f.read()

            # Reemplazar marcador específico si existe
            marcador = '<!-- SERVER_PRODUCTS -->'
            if marcador in html:
                nuevo_html = html.replace(marcador, items_html)
            else:
                # Si existe un contenedor con id=server-products, reemplazar solo ese bloque
                import re
                pattern_id = r'<div[^>]*class="container-items"[^>]*id="server-products"[^>]*>[\s\S]*?</div>'
                if re.search(pattern_id, html):
                    nuevo_html = re.sub(pattern_id, f'<div class="container-items" id="server-products">{items_html}</div>', html, count=1)
                else:
                    # Fallback: reemplazar la primera ocurrencia del bloque container-items
                    nuevo_html = re.sub(r'<div class="container-items">[\s\S]*?</div>', f'<div class="container-items">{items_html}</div>', html, count=1)

            with open(ruta_html, 'w', encoding='utf-8') as f:
                f.write(nuevo_html)
        except FileNotFoundError:
            # Si no existe el archivo base, crear uno con el HTML generado
            try:
                with open(ruta_html, 'w', encoding='utf-8') as f:
                    f.write(generar_html())
            except Exception:
                pass


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", PORT), TiendaHandler)
    print(f"✅ Servidor activo en: http://localhost:{PORT}")
    servidor.serve_forever()
