///----------------------------------------------------------------------------------///
///                 SISTEMA DE GESTION DE SALUD VETERINARIA EL VALLE                 ///
///                     PORTAFOLIO DUOC UC PUENTE ALTO - GRUPO 2                     ///
///----------------------------------------------------------------------------------///

Integrantes:
            - Paulina Espinoza
            - Sebastián Salgado
            - Marco Pezoa

///----------------------------------------------------------------------------------///
Información relevante del Proyecto:

    Realizado con Frameworkd Django (4.2), Oracle 19c, HTML, CSS, Javascript.
    Revisado en navegadores web Chrome, Edge, Firefox en sus ultimas versiones.

///----------------------------------------------------------------------------------///
Requisitos de instalación previa:
    - Python (v.3.10)
    - Framework Django (v.4.2.1)
    - Motor BDA: Oracle 19c
    - Gestor BDA: SQL Developers.
    - Configuración Django/Oracle: cx-Oracle  (v.8.3.0)

///----------------------------------------------------------------------------------///
Caracteristicas:
Que hace:

    * Gestión de roles y permisos: define y administra los roles (grupos) de usuarios dentro del sistema. Permite crear o modificar un rol de usuario y asignarle permisos de acceso a funcionalidades del sistema.

    * Gestión de usuarios: administra los usuarios del sistema. Permite crear, modificar o eliminar de forma logica a los usuarios del sistema, así como gestionar su información personal, credenciales de inicio de sesión. También puede incluir funcionalidades como recuperación de contraseña y administración de perfiles de usuario. Permite la gestión de empleados y clientes desde el menú de adminstrador, y solo clientes desde el menú de recepcionista.

    * Gestión de pacientes:  administrar la información de los pacientes (mascotas) del centro veterinario. Permite registrar y mantener actualizados los datos de los animales atendidos, como su especie, raza, edad, historial médico, vacunas y tratamientos recibidos. Permite tener acceso al historial de atenciones medicas desde el menú de la mascota.

    * Gestión de citas: Permite la programación y gestión de las citas de los pacientes. Permite registrar nuevas citas, asignar pacientes, definir horarios y fecha de agendamiento, así como gestionar la disponibilidad de los veterinarios de acuerdo al horario seleccionado. También incluye las funciones de notificación de agendamiento de citas y la capacidad de reprogramar o cancelar citas existentes.

    * Gestión de consultas médicas: Permite registrar y gestionar las consultas médicas realizadas a los pacientes. Permite capturar información detallada sobre cada consulta, como el motivo de la consulta, diagnóstico, tratamiento recomendado y observaciones adicionales, asi como también el calculo del IMC (índice de masa corporal) del paciente. También incluye la capacidad de adjuntar archivos o resultados de pruebas médicas.

    * Gestión de proveedores: Permite administrar la información de los proveedores de productos e insumos veterinarios. Permite mantener un registro de los proveedores y sus datos de contacto.

    Gestión de productos: Permite administrar el inventario de productos del centro veterinario. Permite registrar los productos disponibles, sus características, precios, niveles de existencia y proveedores asociados. También incluye funciones de control de stock y registro de movimientos de inventario con notificación al correo electronico del administrador cuando los productos se encuentren bajo el stock minimo.

    * Gestión de servicios: Permite administrar los servicios ofrecidos por el centro veterinario, como consultas, vacunaciones, cirugías, análisis clínicos, entre otros. Permite definir y mantener una lista de servicios disponibles, sus descripciones y costos de atención.

    * Gestión de reportes: Permite generar informes y reportes relacionados con diferentes aspectos del centro veterinario, como informes de atención (consulta médica), total de atenciones, total de clientes y pacientes registrados entre un periodo de fechas. Permite generar informes personalizados basados en los datos almacenados en el sistema y ofrece una herramienta de exportación de datos en formato XLS y PDF para facilitar el análisis y la toma de decisiones. Esta opción se encuentra disponible en el menú Clientes, Pacientes y Consulta Médica.

    * Acceso de clientes: Permite el acceso para propietarios de mascotas, donde pueden acceder a información relevante sobre sus mascotas, programar citas, ver el historial clinico de atenciones de sus mascotas.


Que no hace:

    * Facturación y gestión de pagos: El sistema no aborda la funcionalidad de facturación y gestión de pagos. Esto implica la generación de facturas para los servicios prestados, la gestión de pagos de los clientes y la generación de informes financieros.

    * Programación de cirugías y procedimientos: El sistema no contempla la gestión de programación de cirugías u otros procedimientos médicos que requieren una planificación detallada y coordinación de recursos.

    * Funcionalidades específicas de laboratorio: El sistema no incluye funcionalidades específicas para el manejo de laboratorios, como seguimiento de muestras, generación de resultados de pruebas, integración con equipos de laboratorio, entre otros.

    * Funcionalidades de marketing y comunicación: No incluye características relacionadas con el marketing y la comunicación, como campañas de correo electrónico, recordatorios automáticos de citas, gestión de redes sociales, entre otros.

    * Integración con equipos médicos: Si bien el sistema cuenta con información sobre servicios y tratamientos, no incluye una integración directa con equipos médicos específicos, como equipos de diagnóstico por imágenes o equipos de monitoreo de pacientes.


///----------------------------------------------------------------------------------///
GUIA PARA LA INSTALACIÓN DE LA APLICACIÓN:

1.- Asegúrate de tener Oracle instalado y los servicios de la base de datos Oracle activos.

2.- Abre una terminal cmd y navega hasta el directorio raíz del proyecto Django.

3.- Activa tu entorno virtual. Puedes hacerlo ejecutando el siguiente comando:
    En Windows: venv\Scripts\activate
    En macOS/Linux: source venv/bin/activate

4.- Asegúrate de tener todas las dependencias de Django y Oracle instaladas. Puedes hacerlo ejecutando el siguiente comando en el entorno virtual activado:
    pip install django cx_Oracle

5.-En SQL Developer, inicie sesión con system, Debera indicar el nombre de usuario (system) y la contraseña que configuró en la base de datos la primera vez.

6.- Utilice el siguiente script para crear el usuario configurado en el proyecto y la contraseña para establecer la conexion con la BD
    
    alter session set "_ORACLE_SCRIPT" = True;
    create user c##grupo2 identified by grupo2;
    grant connect, resource to c##grupo2;
    alter user c##grupo2 default tablespace users quota unlimited on users;


7.-Migrar los datos a la base de datos Oracle. Ejecuta el siguiente comando en la terminal para aplicar las migraciones pendientes:
    python manage.py migrate

8.-Finalmente, ejecuta el servidor de desarrollo de Django con el siguiente comando:
    python manage.py runserver

9.-Esto iniciará el servidor de desarrollo y podrás acceder a la aplicación Django en tu navegador visitando la dirección http://localhost:8000/ o la dirección que se muestre en la terminal.

10.- Ahora, en SQL Developer Oracle cree una nueva conexion con los datos ingresados anteriormente. Nombre de usuario c##grupo2 y contraseña grupo2. cambiar el SID por orcl, probar y conectar.

11.- Abra la conexión creada y Ejecute en SQL Developer Oracle el Script de poblado de tablas.sql en la conexión a la base de datos del proyecto(grupo2) para crear los procedimientos almacenados y cargar los datos en la BD.

12.-Ahora pruebe el proyecto.



/******************************************* Otorgar permisos en las vistas ************************************************/
/*
    Como administrador se debe crear los permisos y los grupos administrador, cliente, veterinario y recepcionista dando clic al boton 
    otorgar permisos, esto permitira que se asignen inmediatamente los permisos dependiendo del tipo de rol y de usuario al cual pertenezca

*/

/********************************************************************************************************************/


/****************************Datos de prueba de acceso a la plataforma **********************************
Usuario Administrador:
    rut: 11.879.442-7	
    clave: adminadmin

Usuario Recepcionista:
    rut: 8.240.453-8
    clave: adminadmin

Usuario Veterinario:
    rut: 24.881.275-3
    clave: adminadmin

Usuario Cliente:
    rut: 14.479.215-7
    clave: adminadmin

/*********************************************************************************************