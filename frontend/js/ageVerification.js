
export function verifyAge() {
    return Swal.fire({
      title: "Confirmar edad",
      confirmButtonColor: "#000000",
      text: "¿Es mayor de 18 años?",
      confirmButtonText: "Sí, soy mayor de 18 años",
      showCancelButton: true,
      cancelButtonText: "No, soy menor de 18 años",
    });
  }
  