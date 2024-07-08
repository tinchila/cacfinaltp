// main.js
import { verifyAge } from './ageVerification.js';
import { registerUser } from './registration.js';
import { loginUser } from './login.js';

document.addEventListener("DOMContentLoaded", async function () {
  const result = await verifyAge();
  if (result.isConfirmed && result.value) {
    Swal.fire({
      title: "Bienvenido a la tienda de La Bodega",
      text: "Vinoteca Online",
      customClass: {
        confirmButton: "estilo-boton",
      },
    });

    registerUser();
    loginUser();

    // Clase Producto
    class Producto {
      constructor(id, bebida, marca, variedad, precio, img, cantidad) {
        this.id = id;
        this.bebida = bebida;
        this.marca = marca;
        this.variedad = variedad;
        this.precio = precio;
        this.img = img;
        this.cantidad = cantidad;
      }
    }

    // Función para obtener productos desde el backend
    const obtenerProductos = async () => {
      try {
        const response = await fetch("https://cac-trabajofinal.onrender.com/api/bebidas");
        const data = await response.json();
        return data.map((producto) => {
          return {
            id: producto.id,
            bebida: producto.bebida,
            marca: producto.marca,
            variedad: producto.variedad,
            precio: producto.precio,
            img: producto.imagen,
            cantidad: producto.cantidad,
          };
        });
      } catch (error) {
        console.error("Error al obtener productos:", error);
        return [];
      }
    };

    // Mostrar Productos
    const showProductos = async () => {
      const productos = await obtenerProductos();
      const contenedorProductos = document.getElementById("contenedorProductos");
      contenedorProductos.innerHTML = ""; // Limpiar el contenedor antes de agregar productos
      productos.forEach((producto) => {
        const card = document.createElement("div");
        card.classList.add("col-xl-3", "col-md-6");
        card.innerHTML = `
          <div class="card">
            <img src="${producto.img}" class="card-img-top imgProductos" alt="${producto.bebida}">
            <div>
              <h5>${producto.bebida}</h5>
              <h5>${producto.marca}</h5>
              <h5>${producto.variedad}</h5>
              <p>${producto.precio}</p>
              <button class="btn colorBoton" id="boton${producto.id}">Agregar al Carrito</button>
            </div>
          </div>
        `;
        contenedorProductos.appendChild(card);

        const boton = document.getElementById(`boton${producto.id}`);
        boton.addEventListener("click", () => {
          addCarrito(producto.id, productos);
          const Toast = Swal.mixin({
            toast: true,
            position: "top-end",
            showConfirmButton: false,
            timer: 1000,
            timerProgressBar: true,
            didOpen: (toast) => {
              toast.addEventListener("mouseenter", Swal.stopTimer);
              toast.addEventListener("mouseleave", Swal.resumeTimer);
            },
          });
          Toast.fire({
            icon: "success",
            title: "Agregaste el producto al carrito de compras",
          });
        });
      });
    };

    showProductos();

    let carrito = JSON.parse(localStorage.getItem("carrito")) || []; // Obtener carrito desde localStorage

    // Función Agregar al Carrito
    const addCarrito = (id, productos) => {
      const productoEnCarrito = carrito.find((producto) => producto.id === id);
      if (!productoEnCarrito) {
        const producto = productos.find((producto) => producto.id === id);
        if (producto) {
          // Agregar el producto con cantidad inicial 1
          carrito.push(
            new Producto(
              producto.id,
              producto.bebida,
              producto.marca,
              producto.variedad,
              producto.precio,
              producto.img,
              1 // Cantidad inicial
            )
          );
          localStorage.setItem("carrito", JSON.stringify(carrito)); // Actualizar carrito en localStorage
        }
      } else {
        // Incrementar cantidad del producto en el carrito
        productoEnCarrito.cantidad++;
        localStorage.setItem("carrito", JSON.stringify(carrito)); // Actualizar carrito en localStorage
      }
      mostrarCarrito();
    };

    // Mostrar Carrito
    const mostrarCarrito = () => {
      const contenedorCarrito = document.getElementById("contenedorCarrito");
      contenedorCarrito.innerHTML = ""; // Limpiar el contenedor antes de agregar productos
      carrito.forEach((producto) => {
        const card = document.createElement("div");
        card.classList.add("col-12", "col-md-6", "col-lg-4");
        card.innerHTML = `
          <div class="card mb-3">
            <img src="${producto.img}" class="card-img-top" alt="${producto.bebida}">
            <div class="card-body">
              <h5 class="card-title">${producto.bebida}</h5>
              <p class="card-text">Marca: ${producto.marca}</p>
              <p class="card-text">Variedad: ${producto.variedad}</p>
              <p class="card-text">Precio: ${producto.precio}</p>
              <p class="card-text">Cantidad: ${producto.cantidad}</p>
              <button class="btn btn-danger" onclick="eliminarProducto(${producto.id})">Eliminar</button>
            </div>
          </div>
        `;
        contenedorCarrito.appendChild(card);
      });
      actualizarTotal();
    };

    // Eliminar Producto del Carrito
    window.eliminarProducto = (id) => {
      carrito = carrito.filter((producto) => producto.id !== id);
      localStorage.setItem("carrito", JSON.stringify(carrito)); // Actualizar carrito en localStorage
      mostrarCarrito();
    };

    // Vaciar Carrito
    document.getElementById("vaciarCarrito").addEventListener("click", () => {
      carrito = [];
      localStorage.removeItem("carrito"); // Eliminar carrito de localStorage
      mostrarCarrito();
    });

    // Finalizar Compra
    document.getElementById("finalizarCompra").addEventListener("click", () => {
      Swal.fire({
        title: "Compra realizada",
        text: "Gracias por tu compra!",
        icon: "success",
        confirmButtonColor: "#000000",
      });
      carrito = [];
      localStorage.removeItem("carrito"); // Eliminar carrito de localStorage
      mostrarCarrito();
    });

    // Actualizar Total
    const actualizarTotal = () => {
      const total = carrito.reduce((acc, producto) => acc + producto.precio * producto.cantidad, 0);
      document.getElementById("total").innerText = total;
    };

    // Ver Carrito
    document.getElementById("verCarrito").addEventListener("click", mostrarCarrito);

    // Inicializar Carrito al cargar la página
    mostrarCarrito();
  } else {
    Swal.fire({
      title: "Acceso denegado",
      text: "Debes ser mayor de 18 años para acceder a esta tienda.",
      icon: "warning",
      confirmButtonColor: "#000000",
    });
  }
});
