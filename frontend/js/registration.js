class Usuarios {
    constructor(email, clave, nombre, apellido) {
      this.email = email;
      this.clave = clave;
      this.nombre = nombre;
      this.apellido = apellido;
    }
  }
  
  let listaDeUsuarios = JSON.parse(localStorage.getItem("listaDeUsuarios")) || [];
  
  export function registerUser() {
    const singUp = document.getElementById("singUp");
    singUp.addEventListener("click", () => {
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
            Swal.showValidationMessage(
              "Por favor, complete todos los campos"
            );
          }
  
          return { email, clave, nombre, apellido };
        },
      }).then((result) => {
        if (result.isConfirmed) {
          const { email, clave, nombre, apellido } = result.value;
          Swal.fire("Usuario creado");
          const nuevoUsuario = new Usuarios(email, clave, nombre, apellido);
          listaDeUsuarios.push(nuevoUsuario);
          localStorage.setItem(
            "listaDeUsuarios",
            JSON.stringify(listaDeUsuarios)
          );
        }
      });
    });
  }
  