export function loginUser() {
    const singIn = document.getElementById("singIn");
    singIn.addEventListener("click", () => {
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
            Swal.showValidationMessage(
              "Por favor, ingrese usuario y contraseña"
            );
          }
  
          return { login, password };
        },
      }).then((result) => {
        if (result.isConfirmed) {
          const { login, password } = result.value;
          const storedUsers = JSON.parse(
            localStorage.getItem("listaDeUsuarios")
          );
          const user = storedUsers.find((usuario) => usuario.email === login);
  
          if (!user) {
            Swal.fire(
              "Usuario no encontrado",
              "Debe registrarse para poder realizar una compra",
              "error"
            );
          } else {
            let intentosRestantes = 3;
            let loginExitoso = false;
            while (intentosRestantes > 0 && !loginExitoso) {
              if (user.clave === password) {
                Swal.fire("Inicio de Sesión Correcto", "", "success");
                loginExitoso = true;
                break;
              } else {
                intentosRestantes--;
                if (intentosRestantes === 0) {
                  Swal.fire(
                    "Has agotado todos los intentos posibles",
                    "Vuelve a iniciar sesión",
                    "error"
                  );
                  return;
                } else {
                  Swal.fire(
                    `Clave incorrecta. Te quedan ${intentosRestantes} intentos restantes.`
                  );
                  return { login, password };
                }
              }
            }
          }
        }
      });
    });
  }
  