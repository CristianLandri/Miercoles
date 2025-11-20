// ===============================
//      CARRITO DE COMPRAS
// ===============================

// Cargar carrito desde localStorage o crear uno vacío
let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

// Guardar carrito en localStorage
function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
}

// ===============================
//      AGREGAR PRODUCTO
// ===============================
function agregarAlCarrito(id, nombre, precio, imagen) {
    let producto = carrito.find(p => p.id === id);

    if (producto) {
        producto.cantidad++;
    } else {
        carrito.push({
            id: id,
            nombre: nombre,
            precio: precio,
            imagen: imagen,
            cantidad: 1
        });
    }

    guardarCarrito();
    mostrarCarrito();
}

// ===============================
//      ELIMINAR PRODUCTO
// ===============================
function eliminarProducto(id) {
    carrito = carrito.filter(p => p.id !== id);
    guardarCarrito();
    mostrarCarrito();
}

// ===============================
//      SUMAR CANTIDAD
// ===============================
function sumar(id) {
    let p = carrito.find(x => x.id === id);
    if (p) p.cantidad++;
    guardarCarrito();
    mostrarCarrito();
}

// ===============================
//      RESTAR CANTIDAD
// ===============================
function restar(id) {
    let p = carrito.find(x => x.id === id);
    if (p) {
        p.cantidad--;
        if (p.cantidad <= 0) eliminarProducto(id);
    }
    guardarCarrito();
    mostrarCarrito();
}

// ===============================
//      MOSTRAR CARRITO EN HTML
// ===============================
function mostrarCarrito() {
    const cont = document.getElementById("carrito");
    const totalHTML = document.getElementById("total");

    if (!cont) return; // por si no existe en algunas páginas

    cont.innerHTML = "";

    let total = 0;

    carrito.forEach(p => {
        total += p.precio * p.cantidad;

        cont.innerHTML += `
            <div class="item-carrito">
                <img src="${p.imagen}" class="img-carrito">
                <div class="info-carrito">
                    <h3>${p.nombre}</h3>
                    <p>$${p.precio}</p>
                    <div class="controles">
                        <button onclick="restar(${p.id})">-</button>
                        <span>${p.cantidad}</span>
                        <button onclick="sumar(${p.id})">+</button>
                    </div>
                    <button class="eliminar" onclick="eliminarProducto(${p.id})">Eliminar</button>
                </div>
            </div>
        `;
    });

    totalHTML.innerText = "Total: $" + total;
}

// ===============================
//      LIMPIAR CARRITO
// ===============================
function vaciarCarrito() {
    carrito = [];
    guardarCarrito();
    mostrarCarrito();
}

// ===============================
//      INICIALIZAR
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    mostrarCarrito();
});
