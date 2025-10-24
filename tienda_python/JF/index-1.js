// Variables
let carrito = [];
const contador = document.getElementById("contador-productos");
const containerCart = document.querySelector(".container-cart-products");
const totalPagar = document.querySelector(".total-pagar");

// Función para actualizar el contador
function actualizarContador() {
  contador.textContent = carrito.reduce((acc, prod) => acc + prod.cantidad, 0);
}

// Función para actualizar la vista del carrito
function actualizarCarrito() {
  const carritoContainer = containerCart.querySelector(".cart-total").previousElementSibling;
  carritoContainer.innerHTML = ""; // Limpiar productos anteriores

  carrito.forEach((prod, index) => {
    const div = document.createElement("div");
    div.classList.add("row-product");
    div.innerHTML = `
      <div class="cart-product">
        <span class="cantidad-producto-carrito">${prod.cantidad}</span>
        <p class="titulo-producto-carrito">${prod.nombre}</p>
        <span class="precio-producto-carrito">$${prod.precio}</span>
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
        class="icon-close">
        <path stroke-linecap="round" stroke-linejoin="round"
          d="M6 18L18 6M6 6l12 12"/>
      </svg>
    `;
    carritoContainer.appendChild(div);

    // Botón eliminar producto
    div.querySelector(".icon-close").addEventListener("click", () => {
      carrito.splice(index, 1);
      actualizarContador();
      actualizarCarrito();
    });
  });

  // Actualizar total
  const total = carrito.reduce((acc, prod) => acc + prod.precio * prod.cantidad, 0);
  totalPagar.textContent = `$${total}`;
}

// Agregar eventos a los botones
const botones = document.querySelectorAll(".btn-add-cart");
botones.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const item = e.target.closest(".item");
    const nombre = item.querySelector("h2").textContent;
    const precio = parseFloat(item.querySelector(".price").textContent.replace("$", ""));

    // Revisar si ya está en el carrito
    const productoExistente = carrito.find((p) => p.nombre === nombre);
    if (productoExistente) {
      productoExistente.cantidad += 1;
    } else {
      carrito.push({ nombre, precio, cantidad: 1 });
    }

    // Mostrar carrito
    containerCart.classList.remove("hidden-cart");
    actualizarContador();
    actualizarCarrito();
  });
});

// Mostrar / ocultar carrito al tocar icono
const iconCart = document.querySelector(".icon-cart");
iconCart.addEventListener("click", () => {
  containerCart.classList.toggle("hidden-cart");
});
