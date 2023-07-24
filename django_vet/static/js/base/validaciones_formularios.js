document.cookie = 'cookieName=cookieValue; SameSite=Lax';

document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los campos y elementos de mensaje de error
    var usernameInput = document.getElementById('username-input');
    var usernameError = document.getElementById('username-error');
    var firstNameInput = document.getElementById('first-name-input');
    var firstNameError = document.getElementById('first-name-error');
    var lastNameInput = document.getElementById('last-name-input');
    var lastNameError = document.getElementById('last-name-error');
    var emailInput = document.getElementById('email-input');
    var emailError = document.getElementById('email-error');
    var direccionInput = document.getElementById('direccion-input');
    var direccionError = document.getElementById('direccion-error');
    var telefonoInput = document.getElementById('telefono-input');
    var telefonoError = document.getElementById('telefono-error');

    // var nombreEmpresaInput = document.getElementById('nombre-empresa-input');
    // var nombreEmpresaError = document.getElementById('nombre-empresa-error');

    // var nombreContactoInput = document.getElementById('nombre-contacto-input');
    // var nombreContactoError = document.getElementById('nombre-contacto-error');
       
    
// Validar el campo de nombre de usuario
    usernameInput.addEventListener('input', function() {
        var usernameValue = usernameInput.value.trim(); // Eliminar espacios en blanco al inicio y al final

        if (usernameValue.length < 3) {
            usernameError.style.display = 'block';
            usernameError.textContent = 'El nombre de usuario debe tener al menos 3 caracteres';
            usernameInput.classList.remove('is-valid'); // Remover la clase de éxito
            usernameInput.classList.add('is-invalid');
        } else if (!/^[a-zA-Z0-9@./+/_-]+$/.test(usernameValue)) {
            usernameError.style.display = 'block';
            usernameError.textContent = 'Este campo solo debe contener letras, números y los caracteres @/./+/-/_';
            usernameInput.classList.remove('is-valid'); // Remover la clase de éxito
            usernameInput.classList.add('is-invalid');
        } else {
            usernameError.style.display = 'none';
            usernameInput.classList.remove('is-invalid');
            usernameInput.classList.add('is-valid'); // Agregar la clase de éxito

            // Mostrar el ícono de éxito
            var successIcon = document.getElementById('username-success-icon');
            successIcon.style.display = 'inline';
        }
    });

// Validar el campo de nombre de usuario
    firstNameInput.addEventListener('input', function() {
        var firstNameValue = firstNameInput.value.trim(); // Eliminar espacios en blanco al inicio y al final

        if (firstNameValue.length < 3) {
            firstNameError.style.display = 'block';
            firstNameError.textContent = 'El nombre debe tener al menos 3 caracteres';
            firstNameInput.classList.remove('is-valid'); // Remover la clase de éxito
            firstNameInput.classList.add('is-invalid');
        } else if (!/^[a-zA-ZñÑáÁéÉíÍóÓúÚ\s]+$/.test(firstNameValue)) {
            firstNameError.style.display = 'block';
            firstNameError.textContent = 'Por favor, ingresa un nombre válido (solo letras)';
            firstNameInput.classList.remove('is-valid'); // Remover la clase de éxito
            firstNameInput.classList.add('is-invalid');
        } else {
            firstNameError.style.display = 'none';
            firstNameInput.classList.remove('is-invalid');
            firstNameInput.classList.add('is-valid'); // Agregar la clase de éxito

            // Mostrar el ícono de éxito
            var successIcon = document.getElementById('firstName-success-icon');
            successIcon.style.display = 'inline';
        }
    });

// Validar el campo de apellido de usuario
    lastNameInput.addEventListener('input', function() {
        var lastNameValue = lastNameInput.value.trim(); // Eliminar espacios en blanco al inicio y al final
    
        if (lastNameValue.length < 3) {
            lastNameError.style.display = 'block';
            lastNameError.textContent = 'El apellido debe tener al menos 3 caracteres';
            lastNameInput.classList.remove('is-valid'); // Remover la clase de éxito
            lastNameInput.classList.add('is-invalid');
        } else if (!/^[a-zA-ZñÑáÁéÉíÍóÓúÚ\s]+$/.test(lastNameValue)) {
            lastNameError.style.display = 'block';
            lastNameError.textContent = 'Por favor, ingresa un apellido válido (solo letras)';
            lastNameInput.classList.remove('is-valid'); // Remover la clase de éxito
            lastNameInput.classList.add('is-invalid');
        } else {
            lastNameError.style.display = 'none';
            lastNameInput.classList.remove('is-invalid');
            lastNameInput.classList.add('is-valid'); // Agregar la clase de éxito
    
            // Mostrar el ícono de éxito
            var successIcon = document.getElementById('lastName-success-icon');
            successIcon.style.display = 'inline';
        }
    });
    
// Validar el campo de correo eléctronico
    emailInput.addEventListener('input', function() {
        if (!/^[\w.-]+@[a-zA-Z_-]+?(?:\.[a-zA-Z]{2,})+$/.test(emailInput.value)) {
            emailError.style.display = 'block';
            emailError.textContent = 'Por favor, ingresa un correo válido (ejemplo: ejemplo@dominio.com)';
            emailInput.classList.remove('is-valid'); // Remover la clase de éxito
            emailInput.classList.add('is-invalid');
        } else {
            emailError.style.display = 'none';
            emailInput.classList.remove('is-invalid');
            emailInput.classList.add('is-valid'); // Agregar la clase de éxito

            // Mostrar el ícono de éxito
            var successIcon = document.getElementById('email-success-icon');
            successIcon.style.display = 'inline';
        }
    });



// Validar el campo de telefono
    telefonoInput.addEventListener('input', function() {
        if (!/^\+56[1-9][0-9]{8}$/.test(telefonoInput.value)) {
            telefonoError.style.display = 'block';
            telefonoError.textContent = 'Por favor, ingresa un número de teléfono válido (ejemplo: +56912345678)';
            telefonoInput.classList.remove('is-valid'); // Remover la clase de éxito
            telefonoInput.classList.add('is-invalid');
        } else {
            telefonoError.style.display = 'none';
            telefonoInput.classList.remove('is-invalid');
            telefonoInput.classList.add('is-valid'); // Agregar la clase de éxito

            // Mostrar el ícono de éxito
            var successIcon = document.getElementById('telefono-success-icon');
            successIcon.style.display = 'inline';
        }
    });



// Validar el campo de dirección
    direccionInput.addEventListener('input', function() {
        var direccionValue = direccionInput.value.trim(); // Eliminar espacios en blanco al inicio y al final
    
        if (direccionValue.length < 3) {
            direccionError.style.display = 'block';
            direccionError.textContent = 'La dirección debe tener al menos 3 caracteres';
            direccionInput.classList.remove('is-valid'); // Remover la clase de éxito
            direccionInput.classList.add('is-invalid');
        } else if (!/^[a-zA-Z0-9#-\s]+$/.test(direccionInput.value)) {
            direccionError.style.display = 'block';
            direccionError.textContent = 'Por favor, ingresa una dirección válida (solo letras, números y el carácter #)';
            direccionInput.classList.remove('is-valid'); // Remover la clase de éxito
            direccionInput.classList.add('is-invalid');
        } else {
            direccionError.style.display = 'none';
            direccionInput.classList.remove('is-invalid');
            direccionInput.classList.add('is-valid'); // Agregar la clase de éxito
    
            // Mostrar el ícono de éxito
            var successIcon = document.getElementById('direccion-success-icon');
            successIcon.style.display = 'inline';
        }
    });

    

  });



