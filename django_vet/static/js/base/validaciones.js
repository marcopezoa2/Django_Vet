document.cookie = 'cookieName=cookieValue; SameSite=Lax';

// Se llama al campo 'name' de los inputs.
const nombreNameField = document.querySelector('[name=nombre]');
const correoNameField = document.querySelector('[name=correo]');
const asuntoNameField = document.querySelector('[name=asunto]');
const mensajeNameField = document.querySelector('[name=mensaje]');
// Campo de tipo imagen
const imagenNameField = document.querySelector('[name=imagen]');

// Funcion que valida campos vacios
const validarCamposVacios = (message, e) => {
    // 'field' captura el campo input
    const field =e.target;
    // 'fieldValue' captura el valor que toma tiene el input.
    const fieldValue = e.target.value;

    if(fieldValue.trim().length === 0){
        // Agrega el mensaje de error
        field.classList.add('border-error');
        field.nextElementSibling.classList.add('error');
        field.nextElementSibling.innerText = message;
    } else {
        // Quita el mensaje de error
        field.classList.remove('border-error');
        field.nextElementSibling.classList.remove('error');
        field.nextElementSibling.innerText = '';
    }
};

// Funcion que valida el correo
const validarCorreo = (e) => {
    // 'field' captura el campo input
    const field =e.target;
    // 'fieldValue' captura el valor que toma tiene el input.
    const fieldValue = e.target.value;
    // Expresion regular que valida correo
    const emailRegex = /^([A-Z|a-z|0-9](\.|_){0,1})+[A-Z|a-z|0-9]\@([A-Z|a-z|0-9])+((\.){0,1}[A-Z|a-z|0-9]){2}\.[a-z]{2,3}$/;

    if(fieldValue.trim().length > 5 && !emailRegex.test(field.value)){
        // Agrega el mensaje de error
        field.classList.add('border-error');
        field.nextElementSibling.classList.add('error');
        field.nextElementSibling.innerText = 'Ingresa un correo valido';
    } else {
        // Quita el mensaje de error 
        field.classList.remove('border-error');
        field.nextElementSibling.classList.remove('error');
        field.nextElementSibling.innerText = '';
    }
};

// Funcion que valida letras
const validarLetras = (e) => {
    // 'field' captura el campo input
    const field =e.target;

    // Expresion regular que valida texto
    const regex = new RegExp(/^[A-Za-zÁÉÍÓÚÜáéíóúü\s]+$/);

    if(!regex.test(field.value)){
        // Agrega el mensaje de error
        field.classList.add('border-error');
        field.nextElementSibling.classList.add('error');
        field.nextElementSibling.innerText = 'Este campo solo acepta letras';
    } else {
        // Quita el mensaje de error 
        field.classList.remove('border-error');
        field.nextElementSibling.classList.remove('error');
        field.nextElementSibling.innerText = '';
    }
};

// Envio de mensaje de error para campos vacios
nombreNameField.addEventListener('blur', (e) => validarCamposVacios('Por favor, ingresa tu nombre', e));
correoNameField.addEventListener('blur', (e) => validarCamposVacios('Por favor, ingresa tu correo', e));
asuntoNameField.addEventListener('blur', (e) => validarCamposVacios('Por favor, ingresa el asunto', e));
mensajeNameField.addEventListener('blur', (e) => validarCamposVacios('Por favor, ingresa el mensaje', e));

// Para validar el ingreso de un correo valido
correoNameField.addEventListener('input', validarCorreo);

// Para validar el ingreso de texto valido
nombreNameField.addEventListener('input', validarLetras);
asuntoNameField.addEventListener('input', validarLetras);

// Extra => validacion campo FILE de imagenes (Al igual que el SELECT no permite la insercion de texto)
// Usa 'change' cuando el campo ha cambiado -> Tambien se usa con 'SELECT'
imagenNameField.addEventListener('change', (e) => {
    // 'field' captura el campo input
    const field =e.target;

    // Extrae la extension de 1 archivo con el 'name'
    const fileExtension = e.target.files[0].name.split('.').pop().toLowerCase();
    const extensiones = ['jpg', 'jpeg', 'png', 'gif'];

    if(!extensiones.include(fileExtension)) {
        // Agrega el mensaje de error
        field.classList.add('border-error');
        field.nextElementSibling.classList.add('error');
        field.nextElementSibling.innerText = `Las extensiones permitidas son: ${extensiones.join(', ')}`;
    } else {
        // Quita el mensaje de error 
        field.classList.remove('border-error');
        field.nextElementSibling.classList.remove('error');
        field.nextElementSibling.innerText = '';
    }

});





