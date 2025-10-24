from http.server import SimpleHTTPRequestHandler, HTTPServer
import sqlite3
import os

# 📦 Ruta del archivo de base de datos
DB_PATH = "tienda.db"

# ⚙️ Crear base de datos si no existe
def inicializar_base():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            imagen_url TEXT NOT NULL
        )
        """)
        # Agregamos productos de ejemplo
        cursor.execute("INSERT INTO productos (nombre, precio, imagen_url) VALUES ('Manzana', 1200, 'img/manzanero.jpg')")
        cursor.execute("INSERT INTO productos (nombre, precio, imagen_url) VALUES ('Naranja', 800, 'img/Naranja.jpg')")
        cursor.execute("INSERT INTO productos (nombre, precio, imagen_url) VALUES ('Perejil', 500, 'img/Perejil.jpg')")
        conn.commit()
        conn.close()
        print("✅ Base de datos creada con productos de ejemplo.")
    else:
        print("📁 Base de datos encontrada.")

# 🗃️ Función para obtener los productos
def obtener_productos():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder por nombre
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

# 🧱 Genera el HTML dinámico
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
        <link rel="stylesheet" type="text/css" href="css/tienda.css">
    </head>
    <body>
        <header>
            <div class="btn-menu"><label for="btn-menu">☰</label></div>
            <h1>AgroSt❀r Tienda☀</h1>

            <div class="container-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                    class="icon-cart">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993
                        l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25
                        a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125
                        0 015.513 7.5h12.974c.576 0 1.059.435
                        1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0
                        .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0
                        .375.375 0 01.75 0z"/>
                </svg>
                <div class="count-products">
                    <span id="contador-productos">0</span>
                </div>
            </div>
        </header>

        <input type="checkbox" id="btn-menu">
        <div class="container-menu">
          <div class="cont-menu">
            <nav>
              <a href="Principal.html">Home</a>
              <a href="Plantas.html">Plantas</a>
              <a href="Otro.html">Otros</a>
            </nav>
            <label for="btn-menu">✖️</label>
          </div>
        </div>

        <div class="container-items">
            {items_html}
        </div>

        <script src="JF/index-1.js"></script>
    </body>
    </html>
    """
    return html


# 🌍 Servidor HTTP
class TiendaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            contenido = generar_html().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(contenido)
        else:
            super().do_GET()


if __name__ == "__main__":
    inicializar_base()
    PORT = 5000
    servidor = HTTPServer(("localhost", PORT), TiendaHandler)
    print(f"✅ Servidor activo en: http://localhost:{PORT}")
    servidor.serve_forever()

