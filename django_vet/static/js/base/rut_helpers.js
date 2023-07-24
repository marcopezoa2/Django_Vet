
document.cookie = 'cookieName=cookieValue; SameSite=Lax';

// // rut_helpers.js

function formatRutInput() {
    const rutInput = document.getElementById('rutInput');
    const formattedRut = formatRut(rutInput.value);
    rutInput.value = formattedRut;
    validateRut(rutInput.value);
  }
  
  function formatRut(rut) {
    const cleanRut = rut.replace(/\./g, '').replace(/\-/g, '').trim().toLowerCase();
  
    if (/^\d{1,8}\-\d{1}$/.test(cleanRut)) {
      return cleanRut;
    }
  
    let formattedRut = cleanRut.slice(0, -1);
    const lastDigit = cleanRut.slice(-1);
  
    for (let i = formattedRut.length - 3; i > 0; i -= 3) {
      formattedRut = formattedRut.slice(0, i) + '.' + formattedRut.slice(i);
    }
  
    return formattedRut.concat('-').concat(lastDigit);
  }
  
  function validateRut(rut) {
    const errorElement = document.getElementById('rutError');
    const error = Fn.validaRut(rut);
  
    if (error) {
      errorElement.textContent = error;
    } else {
      errorElement.textContent = '';
    }
  }

  function validateForm() {
    const rutInput = document.getElementById('rutInput');
    const rutError = document.getElementById('rutError');
    const rutValue = rutInput.value.trim();
  
    // Validar el RUT utilizando la función validaRut
    const rutValidationResult = Fn.validaRut(rutValue);
  
    if (rutValidationResult !== null) {
      // Mostrar mensaje de error y evitar el envío del formulario
      rutError.textContent = rutValidationResult;
      Swal.fire({
        icon: 'error',
        title: 'Error en el RUT',
        text: rutValidationResult,
      });
      return false;
    }
  
    return true; // El RUT es válido, se puede enviar el formulario
  }


  var Fn = {
    validaRut: function(rutCompleto) {
      if (!/^[0-9]{1,3}(\.[0-9]{3})*-[0-9kK]{1}$/.test(rutCompleto))
        return "Formato de RUT inválido.";
      
      var tmp = rutCompleto.split('-');
      var rut = tmp[0].replace(/\./g, '');
      var digv = tmp[1];
      digv = digv.toUpperCase()
    
      var reverseRut = rut.split('').reverse();
      var suma = 0;
      var factor = 2;
    
      for (var i = 0; i < reverseRut.length; i++) {
        suma += parseInt(reverseRut[i]) * factor;
        factor = factor === 7 ? 2 : factor + 1;
      }
    
      var dv = 11 - (suma % 11);
      dv = dv === 11 ? '0' : dv === 10 ? 'K' : dv.toString();
    
      if (dv !== digv)
        return "Por favor, ingrese un RUT válido";
    
      return null; // RUT válido
    }
  };