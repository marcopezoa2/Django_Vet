// const form = document.getElementById('formu');
// const nombreField = document.getElementById('nombre');
// const correoField = document.getElementById('correo');
// const asuntoField = document.getElementById('asunto');
// const mensajeField = document.getElementById('mensaje');
// const alerta = document.createElement('div');
// alerta.classList.add('alert', 'alert-danger', 'text-center');

const mostrarError = (field, message) => {
    field.classList.add('border-error');
    field.nextElementSibling.classList.add('error');
    field.nextElementSibling.innerText = message;
  };
  
  const quitarError = (field) => {
    field.classList.remove('border-error');
    field.nextElementSibling.classList.remove('error');
    field.nextElementSibling.innerText = '';
  };
  
  const validarCamposVacios = (field, message) => {
    const fieldValue = field.value.trim();
  
    if (fieldValue === '') {
      mostrarError(field, message);
      return false;
    }
  
    quitarError(field);
    return true;
  };
  
  const validarFormatoCorreo = (field) => {
    const fieldValue = field.value.trim();
    const regex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
  
    if (fieldValue !== '' && !regex.test(fieldValue)) {
      mostrarError(field, 'Ingresa un correo electrónico válido');
      return false;
    }
  
    quitarError(field);
    return true;
  };
  
  const validarTextoNombre = (field) => {
    const fieldValue = field.value.trim();
    const regex = /^[A-Za-zÁÉÍÓÚÜáéíóúü\s]+$/;
  
    if (fieldValue !== '' && !regex.test(fieldValue)) {
      mostrarError(field, 'Este campo solo acepta letras y espacios');
      return false;
    }
  
    quitarError(field);
    return true;
  };
  
  const validarTextoAsunto = (field) => {
    const fieldValue = field.value.trim();
    const regex = /^[\p{L}\s.,'"áéíóúÁÉÍÓÚ()]*[^\d\s][\p{L}\s.,'"áéíóúÁÉÍÓÚ()]*$/u;
  
    if (fieldValue !== '' && !regex.test(fieldValue)) {
      mostrarError(field, 'Este campo solo acepta letras, comas, puntos y comillas');
      return false;
    }
  
    quitarError(field);
    return true;
  };
  
  const validarCamposFormulario = (e) => {
    e.preventDefault();
  
    const camposValidos = [
      validarCamposVacios(nombreField, 'Por favor, ingresa tu nombre'),
      validarCamposVacios(correoField, 'Por favor, ingresa tu correo'),
      validarCamposVacios(asuntoField, 'Por favor, ingresa el asunto'),
      validarCamposVacios(mensajeField, 'Por favor, ingresa el mensaje'),
      validarFormatoCorreo(correoField),
      validarTextoNombre(nombreField),
      validarTextoAsunto(asuntoField)
    ];
  
    const hayErrores = camposValidos.some((valido) => !valido);
  
    if (!hayErrores) {
      const alerta = document.createElement('div');
      alerta.classList.add('alert', 'alert-success', 'text-center');
      alerta.innerText = '¡Formulario enviado con éxito!';
  
      const formulario = document.getElementById('formu');
      formulario.parentNode.insertBefore(alerta, formulario);
  
      setTimeout(() => {
        alerta.remove();
        formulario.reset();
      }, 3000);
    }
  };
  
  const nombreField = document.getElementById('nombre');
  const correoField = document.getElementById('correo');
  const asuntoField = document.getElementById('asunto');
  const mensajeField = document.getElementById('mensaje');
  const botonButton = document.getElementById('enviar');
  
  nombreField.addEventListener('blur', () => validarCamposVacios(nombreField, 'Por favor, ingresa tu nombre'));
  correoField.addEventListener('blur', () => validarCamposVacios(correoField, 'Por favor, ingresa tu correo'));
  asuntoField.addEventListener('blur', () => validarCamposVacios(asuntoField, 'Por favor, ingresa el asunto'));
  mensajeField.addEventListener('blur', () => validarCamposVacios(mensajeField, 'Por favor, ingresa el mensaje'));
  
  nombreField.addEventListener('input', () => validarTextoNombre(nombreField));
  correoField.addEventListener('input', () => validarFormatoCorreo(correoField));
  asuntoField.addEventListener('input', () => validarTextoAsunto(asuntoField));
  
  botonButton.addEventListener('click', validarCamposFormulario);
  


