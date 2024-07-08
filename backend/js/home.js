document.addEventListener('DOMContentLoaded', function () {
    // Verifica si ya se confirmó la edad en esta sesión del navegador
    if (!sessionStorage.getItem('edadConfirmada')) {
        Swal.fire({
            title: "Confirmar edad",
            confirmButtonColor: "#000000",
            text: "¿Es mayor de 18 años?",
            confirmButtonText: "Sí, soy mayor de 18 años",
            showCancelButton: true,
            cancelButtonText: "No, soy menor de 18 años",
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    title: "Bienvenido a La Bodega",
                    text: "Vinoteca Online",
                    customClass: {
                        confirmButton: "estilo-boton",
                    },
                });
                sessionStorage.setItem('edadConfirmada', 'true'); // Guarda la confirmación en sessionStorage
            } else {
                Swal.fire(
                    "Acceso denegado",
                    "Debes ser mayor de 18 años para poder realizar compras en la tienda",
                    "error"
                );
            }
        });
    }

    // Clase para manejar usuarios
    class Usuarios {
        constructor(email, clave, nombre, apellido) {
            this.email = email;
            this.clave = clave;
            this.nombre = nombre;
            this.apellido = apellido;
        }
    }
    let listaDeUsuarios = [];

    // Manejador de evento para registro
    const signUp = document.getElementById("singUp");
    signUp.addEventListener("click", () => {
        Swal.fire({
            title: "Sign Up",
            html: `
                <input type="email" id="email" class="swal2-input" placeholder="Ingrese su email" required>
                <input type="password" id="clave" class="swal2-input" placeholder="Ingrese una clave (mínimo 8 caracteres)" required>
                <input type="text" id="nombre" class="swal2-input" placeholder="Ingrese su nombre" required>
                <input type="text" id="apellido" class="swal2-input" placeholder="Ingrese su apellido" required>
            `,
            focusConfirm: false,
            confirmButtonColor: "#000000",
            preConfirm: () => {
                const email = Swal.getPopup().querySelector("#email").value;
                const clave = Swal.getPopup().querySelector("#clave").value;
                const nombre = Swal.getPopup().querySelector("#nombre").value;
                const apellido = Swal.getPopup().querySelector("#apellido").value;

                if (!email || !clave || !nombre || !apellido) {
                    Swal.showValidationMessage("Por favor, complete todos los campos");
                }

                return { email, clave, nombre, apellido };
            },
        }).then((result) => {
            if (result.isConfirmed) {
                const { email, clave, nombre, apellido } = result.value;
                const nuevoUsuario = new Usuarios(email, clave, nombre, apellido);
                listaDeUsuarios.push(nuevoUsuario);
                localStorage.setItem("listaDeUsuarios", JSON.stringify(listaDeUsuarios));
                Swal.fire("Usuario creado");
            }
        });
    });

    // Manejador de evento para inicio de sesión
    const signIn = document.getElementById("singIn");
    signIn.addEventListener("click", () => {
        Swal.fire({
            title: "Iniciar Sesión",
            html: `
                <input type="text" id="login" class="swal2-input" placeholder="Usuario">
                <input type="password" id="password" class="swal2-input" placeholder="Contraseña">
            `,
            confirmButtonText: "Iniciar Sesión",
            confirmButtonColor: "#000000",
            focusConfirm: false,
            preConfirm: () => {
                const login = Swal.getPopup().querySelector("#login").value;
                const password = Swal.getPopup().querySelector("#password").value;

                if (!login || !password) {
                    Swal.showValidationMessage("Por favor, ingrese usuario y contraseña");
                }

                return { login, password };
            },
        }).then((result) => {
            if (result.isConfirmed) {
                const { login, password } = result.value;
                const storedUsers = JSON.parse(localStorage.getItem("listaDeUsuarios"));
                const user = storedUsers.find((usuario) => usuario.email === login);

                if (!user) {
                    Swal.fire("Usuario no encontrado", "Debe registrarse para poder realizar una compra", "error");
                } else {
                    if (user.clave === password) {
                        Swal.fire("Inicio de Sesión Correcto", "", "success");
                    } else {
                        Swal.fire("Clave incorrecta", "Intente nuevamente", "error");
                    }
                }
            }
        });
    });

    // Manejadores para la barra de navegación responsiva
    const toggleButton = document.getElementById('toggleNavbar');
    const navbarList = document.getElementById('navbarList');

    toggleButton.addEventListener('click', function () {
        if (navbarList.style.display === 'none' || navbarList.style.display === '') {
            navbarList.style.display = 'flex';
        } else {
            navbarList.style.display = 'none';
        }
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth > 1050) {
            navbarList.style.display = 'flex'; // Mostrar la lista de navegación en pantallas grandes
            toggleButton.style.display = 'none'; // Ocultar el botón de dropdown en pantallas grandes
        } else {
            navbarList.style.display = 'none'; // Ocultar la lista de navegación en pantallas pequeñas
            toggleButton.style.display = 'block'; // Mostrar el botón de dropdown en pantallas pequeñas
        }
    });
});
