document.cookie = 'cookieName=cookieValue; SameSite=Lax';
/* --------------------------------------------------- */
/* ------- Capturade los 'id'de cada INPUT ------- */
/* --------------------------------------------------- */
const nombreField = document.getElementById('nombre');
const correoField = document.getElementById('correo');
const asuntoField = document.getElementById('asunto');
const mensajeField = document.getElementById('mensaje');
const botonButton = document.getElementById('btn-enviar');

/* --------------------------------------------------------------- */
/* ----- Funcion para validar que los campos no esten vacios ----- */
/* --------------------------------------------------------------- */
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

/* ---------------------------------------------------------- */
/* ------- Funcion para validar el formato del correo ------- */
/* ---------------------------------------------------------- */
const validarFormatoCorreo = (e) => {
    // Captura el campo input
    const field = e.target;
    // Captura el VALOR del campo
    const fieldValue = e.target.value;
    // Expresion Regular que valida el correo
    const regex = new RegExp(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/);
    // Esta forma de declarar y expresion tb sirven
    // const emailRegex = /^([A-Z|a-z|0-9](\.|_){0,1})+[A-Z|a-z|0-9]\@([A-Z|a-z|0-9])+((\.){0,1}[A-Z|a-z|0-9]){2}\.[a-z]{2,3}$/;

    if(fieldValue.trim().length !== 0){
        if(!regex.test(fieldValue)){
            // Agrega el mensaje de error
            field.classList.add('border-error');
            field.nextElementSibling.classList.add('error');
            field.nextElementSibling.innerText = 'Ingresa un correo electronico valido';
        } else {
            // Quita el mensaje de error
            field.classList.remove('border-error');
            field.nextElementSibling.classList.remove('error');
            field.nextElementSibling.innerText = '';
        }
    };

}; 

/* ---------------------------------------------------------------------------- */
/* ------- Funcion para validar el texto ingresado en el campo 'nombre' ------- */
/* ---------------------------------------------------------------------------- */
const validarTextoNombre = (e) => {
    // Captura el campo input
    const field = e.target;
    // Captura el VALOR del campo
    const fieldValue = e.target.value;
    // Expresion Regular que valida el correo
    const regex = new RegExp(/^[A-Za-zÁÉÍÓÚÜáéíóúü\s]+$/);

    if(fieldValue.trim().length !== 0){
        if(!regex.test(fieldValue)){
            // Agrega el mensaje de error
            field.classList.add('border-error');
            field.nextElementSibling.classList.add('error');
            field.nextElementSibling.innerText = 'Este campo solo acepta letras y espacios';
        } else {
            // Quita el mensaje de error
            field.classList.remove('border-error');
            field.nextElementSibling.classList.remove('error');
            field.nextElementSibling.innerText = '';
        }
    };

};

/* ---------------------------------------------------------------------------- */
/* ------- Funcion para validar el texto ingresado en el campo 'nombre' ------- */
/* ---------------------------------------------------------------------------- */
const validarTextoAsunto = (e) => {
    // Captura el campo input
    const field = e.target;
    // Captura el VALOR del campo
    const fieldValue = e.target.value;
    // Expresion Regular que valida el correo
    const regex = new RegExp(/^[\p{L}\s.,'"áéíóúÁÉÍÓÚ()]*[^\d\s][\p{L}\s.,'"áéíóúÁÉÍÓÚ()]*$/u);

    if(fieldValue.trim().length !== 0){
        if(!regex.test(fieldValue)){
            // Agrega el mensaje de error
            field.classList.add('border-error');
            field.nextElementSibling.classList.add('error');
            field.nextElementSibling.innerText = 'Este campo solo acepta letras, comas, puntos y comillas';
        } else {
            // Quita el mensaje de error
            field.classList.remove('border-error');
            field.nextElementSibling.classList.remove('error');
            field.nextElementSibling.innerText = '';
        }
    };
};

/* ---------------------------------------------------------------------------- */
/* -------- Funcion para validar campos vacios al presionar el 'boton' -------- */
/* ---------------------------------------------------------------------------- */

let alertaVisible = false;

const validarCamposFormulario = (e) => {
    e.preventDefault();

    let hayErrores = false;

    // Verificar si los campos están vacíos
    if (
        nombreField.value.trim().length === 0 ||
        correoField.value.trim().length === 0 ||
        asuntoField.value.trim().length === 0 ||
        mensajeField.value.trim().length === 0
    ) {
        if(!alertaVisible){
            // Se crea el elemento de alerta de Bootstrap
            const alerta = document.createElement('div');
            alerta.classList.add('alert', 'alert-danger', 'text-center');
            alerta.innerText = 'Por favor, completa todos los campos del formulario.';

            // Insertar la alerta antes del formulario
            const formulario = document.getElementById('formu');
            formulario.parentNode.insertBefore(alerta, formulario);

            alertaVisible = true;

            setTimeout(() => {
                alerta.remove();
                alertaVisible = false;
            }, 3000);

        }
    } else {
        // Permite el envío del formulario
        e.target.form.submit();
    }  
};


/* --------------------------------------------------------------------------------------- */
/* ----- Agregar 'Eventos de escucha' a los campos INPUTS y se pasan a las FUNCIONES ----- */
/* --------------------------------------------------------------------------------------- */
// Para validar que los campos no esten vacios
nombreField.addEventListener('blur', (e) => validarCamposVacios('Por favor, ingresa tu nombre', e));
correoField.addEventListener('blur', (e) => validarCamposVacios('Por favor, ingresa tu correo', e));
asuntoField.addEventListener('blur', (e) => validarCamposVacios('Por favor, ingresa el asunto', e));
mensajeField.addEventListener('blur', (e) => validarCamposVacios('Por favor, ingresa el mensaje', e));

// Para validar el ingreso de un correo valido
correoField.addEventListener('input', validarFormatoCorreo);
correoField.addEventListener('blur', validarFormatoCorreo);

// Para validar el Texto del campo 'nombre'
nombreField.addEventListener('blur', validarTextoNombre);

// Para validar el Texto del campo 'asunto'
asuntoField.addEventListener('blur', validarTextoAsunto);

// Agregar evento de clic al botón de enviar
// botonButton.addEventListener('click', validarCamposFormulario);

/* ------------------------- */
/* ----- OBSERVACIONES ----- */
/* ------------------------- */
// 'blur'-> Se activa cuando el campo pierde el foco, después de que el usuario termina de interactuar con un campo ___*
// 'input'-> Se activa inmediatamente después de cualquier cambio en el campo, incluso mientras aún se está escribiendo ___*/
// 'input'-> Se usa en campos donde se requiere validar carater por carater como el 'correo' o 'rut' ___*/











