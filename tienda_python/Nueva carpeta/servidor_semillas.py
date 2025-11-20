from http.server import SimpleHTTPRequestHandler, HTTPServer
import mysql.connector
from urllib.parse import parse_qs, urlparse


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',            
    'password': '',            
    'database': 'tienda_semillas'
}

PORT = 8082  # Puerto diferente para el servidor de semillas


def obtener_productos():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM semillas")  # Cambiado a tabla semillas
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
                <img src="{p['imagen_url']}" alt="semilla">
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
        <title>Tienda de Semillas</title>
        <link rel="stylesheet" href="css/tienda.css">
    </head>
    <body>
        <header>
            <h1>AgroSt❀r Semillas</h1>
        </header>

        <div class="container-items">
            {items_html}
        </div>

        <script src="JF/index-1.js"></script>
    </body>
    </html>
    """
    return html


class SemillasHandler(SimpleHTTPRequestHandler):
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
                self.send_error(400, "ID de semilla requerido")
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
                self.send_error(400, "Faltan datos para actualizar la semilla")
        else:
            self.send_error(404, "Ruta POST no encontrada")

    def mostrar_formulario_edicion(self, id_producto):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM semillas WHERE id = %s", (id_producto,))
        producto = cursor.fetchone()
        conn.close()
        if not producto:
            self.send_error(404, "Semilla no encontrada")
            return
        html = f"""
        <!DOCTYPE html>
        <html lang='es'>
        <head>
            <meta charset='UTF-8'>
            <title>Editar Semilla</title>
            <link rel='stylesheet' href='css/tienda.css'>
        </head>
        <body>
            <h1>Editar Semilla</h1>
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
            "UPDATE semillas SET nombre=%s, descripcion=%s, precio=%s, imagen_url=%s WHERE id=%s",
            (nombre, descripcion, precio, imagen_url, id_producto)
        )
        conn.commit()
        conn.close()


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", PORT), SemillasHandler)
    print(f"✅ Servidor de Semillas activo en: http://localhost:{PORT}")
    servidor.serve_forever()