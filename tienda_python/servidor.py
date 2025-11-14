
from http.server import SimpleHTTPRequestHandler, HTTPServer
import mysql.connector
from urllib.parse import parse_qs, urlparse


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
        items_html += f"""
        <div class="item">
            <figure>
                <img src="{p['imagen_url']}" alt="producto">
            </figure>
            <div class="info-product">
                <h2>{p['nombre']}</h2>
                <p class="price">${p['precio']}</p>
                <p>{p['descripcion'] or ''}</p>
                <a href='/editar?id={p['id']}' class='btn-edit'>Editar</a>
                <button class="btn-add-cart">Añadir al carrito</button>
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
        if self.path == "/" or self.path == "/index.html":
            contenido = generar_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(contenido)
        elif self.path.startswith("/editar"):
            query = urlparse(self.path).query
            params = parse_qs(query)
            id_producto = params.get("id", [None])[0]
            if id_producto:
                self.mostrar_formulario_edicion(id_producto)
            else:
                self.send_error(400, "ID de producto requerido")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/editar"):
            longitud = int(self.headers.get('Content-Length', 0))
            datos = self.rfile.read(longitud).decode('utf-8')
            params = parse_qs(datos)
            id_producto = params.get("id", [None])[0]
            nombre = params.get("nombre", [None])[0]
            descripcion = params.get("descripcion", [None])[0]
            precio = params.get("precio", [None])[0]
            imagen_url = params.get("imagen_url", [None])[0]
            if id_producto and nombre and precio and imagen_url:
                self.actualizar_producto(id_producto, nombre, descripcion, precio, imagen_url)
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_error(400, "Faltan datos para actualizar el producto")
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
                <label>Nombre: <input name='nombre' value='{producto['nombre']}'></label><br>
                <label>Descripción: <textarea name='descripcion'>{producto['descripcion'] or ''}</textarea></label><br>
                <label>Precio: <input name='precio' type='number' step='0.01' value='{producto['precio']}'></label><br>
                <label>Imagen URL: <input name='imagen_url' value='{producto['imagen_url']}'></label><br>
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

    def actualizar_producto(self, id_producto, nombre, descripcion, precio, imagen_url):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, imagen_url=%s WHERE id=%s",
            (nombre, descripcion, precio, imagen_url, id_producto)
        )
        conn.commit()
        conn.close()
        self.actualizar_html_estatico()

    def actualizar_html_estatico(self):
        productos = obtener_productos()
        items_html = ""
        for p in productos:
            items_html += f"""
            <div class='item'>
                <figure>
                    <img src='{p['imagen_url']}' alt='producto'>
                </figure>
                <div class='info-product'>
                    <h2>{p['nombre']}</h2>
                    <p class='price'>${p['precio']}</p>
                    <p>{p['descripcion'] or ''}</p>
                </div>
            </div>
            """
        # Leer el Tienda.html base
        ruta_html = r'g:\PWD\yhoqk\Tienda.html'
        with open(ruta_html, 'r', encoding='utf-8') as f:
            html = f.read()
        # Reemplazar el contenido de <div class="container-items"> ... </div> por los productos actuales
        import re
        nuevo_html = re.sub(r'<div class="container-items">[\s\S]*?</div>', f'<div class="container-items">{items_html}</div>', html, count=1)
        with open(ruta_html, 'w', encoding='utf-8') as f:
            f.write(nuevo_html)


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", PORT), TiendaHandler)
    print(f"✅ Servidor activo en: http://localhost:{PORT}")
    servidor.serve_forever()
