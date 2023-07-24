
/*POBLAMIENTO DE LA BASE DE DATOS*/

/********************************** CREAR PROCEDURE PARA CALCULAR IMC CONSULTA **************************************/
CREATE OR REPLACE PROCEDURE SP_CALCULAR_IMC(
    p_peso IN NUMBER,
    p_altura IN NUMBER,
    p_paciente_id IN NUMBER
) IS
    v_imc NUMBER;
BEGIN
    v_imc := p_peso / (p_altura * p_altura);
    
    -- Actualizar el campo 'imc' en la tabla 'ConsultaMedica' para el paciente específico
    UPDATE CONSULTA_CONSULTAMEDICA
    SET IMC = v_imc
    WHERE paciente_id = p_paciente_id;
    
    COMMIT;
    
    -- Opcional: Retornar el valor del IMC calculado
    DBMS_OUTPUT.PUT_LINE('El IMC calculado es: ' || v_imc);
EXCEPTION
    WHEN OTHERS THEN
        -- Manejar cualquier error que ocurra
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
        ROLLBACK;
END;
/

/********************************** CREAR PROCEDURE PARA LISTAR PRODUCTOS **************************************/
CREATE OR REPLACE PROCEDURE SP_LISTAR_PRODUCTOS
IS
    -- Declarar variables para almacenar los resultados
    CURSOR c_productos IS
        SELECT * FROM INVENTARIO_PRODUCTO;
    -- Variables para almacenar los valores seleccionados
    v_producto INVENTARIO_PRODUCTO%ROWTYPE; -- Puedes ajustar esto según la estructura de tu tabla Producto
BEGIN
    -- Abrir el cursor
    OPEN c_productos;

    -- Recuperar los resultados y almacenarlos en la variable v_producto
    FETCH c_productos INTO v_producto;

    -- Procesar los resultados según sea necesario
    WHILE c_productos%FOUND LOOP
        -- Realiza las operaciones necesarias con los datos de v_producto
        -- Por ejemplo, puedes imprimir los valores de los campos:
        DBMS_OUTPUT.PUT_LINE('ID: ' || v_producto.id || ', Nombre: ' || v_producto.nombre);

        -- Recuperar el siguiente resultado
        FETCH c_productos INTO v_producto;
    END LOOP;

    -- Cerrar el cursor
    CLOSE c_productos;
END;
/


/********************************** ELIMINACIÓN DE SECUENCIAS PARA LOS ID **************************************/
DROP SEQUENCE SEQ_REGION;
DROP SEQUENCE SEQ_COMUNA;
DROP SEQUENCE SEQ_PROVEEDOR;
DROP SEQUENCE SEQ_SERVICIO;
DROP SEQUENCE SEQ_SUSCRIPCION;
DROP SEQUENCE SEQ_CONTACTO;
DROP SEQUENCE SEQ_ESPECIE;
DROP SEQUENCE SEQ_GENERO;
DROP SEQUENCE SEQ_PRODUCTO;
DROP SEQUENCE SEQ_CATEGORIA;
DROP SEQUENCE SEQ_USER;
DROP SEQUENCE SEQ_PACIENTE;
DROP SEQUENCE SEQ_CITA;
DROP SEQUENCE SEQ_CONSULTA;
DROP SEQUENCE SEQ_DESPARASITACION;
DROP SEQUENCE SEQ_VACUNACION;
DROP SEQUENCE SEQ_AUTH_GROUP;
DROP SEQUENCE SEQ_USER_GROUPS;

/********************************** CREACION DE SECUENCIAS PARA LOS ID **************************************/

CREATE SEQUENCE SEQ_AUTH_GROUP START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_USER_GROUPS START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_REGION START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_COMUNA START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_PROVEEDOR START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_SERVICIO START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_SUSCRIPCION START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_CONTACTO START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_ESPECIE START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_GENERO START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_PRODUCTO START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_CATEGORIA START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_USER START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_PACIENTE START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_CITA START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_CONSULTA START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_DESPARASITACION START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE SEQ_VACUNACION START WITH 1 INCREMENT BY 1;


/***************************************** INSERT AUTH_GROUP  **********************************************/
Insert into AUTH_GROUP (ID,NAME) values (SEQ_AUTH_GROUP.NEXTVAL,'Administrador');
Insert into AUTH_GROUP (ID,NAME) values (SEQ_AUTH_GROUP.NEXTVAL,'Recepcionista');
Insert into AUTH_GROUP (ID,NAME) values (SEQ_AUTH_GROUP.NEXTVAL,'Veterinario');
Insert into AUTH_GROUP (ID,NAME) values (SEQ_AUTH_GROUP.NEXTVAL,'Cliente');

/***************************************** INSERT BASE_CONTACTOMODEL  **********************************************/
Insert into BASE_CONTACTOMODEL (ID,NOMBRE,CORREO,ASUNTO,ESTADO,FECHA_CREACION) values (SEQ_CONTACTO.NEXTVAL,'Marco Pezoa','ma.pezoa@duocuc.cl','Consulta','1',to_date('10/06/23','DD/MM/RR'));
Insert into BASE_CONTACTOMODEL (ID,NOMBRE,CORREO,ASUNTO,ESTADO,FECHA_CREACION) values (SEQ_CONTACTO.NEXTVAL,'Paulina Espinoza','pa.espinozao@duocuc.cl','Consulta','1',to_date('15/06/23','DD/MM/RR'));

/***************************************** INSERT BASE_SUSCRIPCIONMODEL  **********************************************/
Insert into BASE_SUSCRIPCIONMODEL (ID,EMAIL,TIMESTAMP,FECHA_CREACION) values (SEQ_SUSCRIPCION.NEXTVAL,'ma.pezoa@duocuc.cl',to_timestamp('12/06/23 04:05:39,241236000','DD/MM/RR HH24:MI:SSXFF'),to_date('12/06/23','DD/MM/RR'));
Insert into BASE_SUSCRIPCIONMODEL (ID,EMAIL,TIMESTAMP,FECHA_CREACION) values (SEQ_SUSCRIPCION.NEXTVAL,'pa.espinozao@duocuc.cl',to_timestamp('13/06/23 04:14:20,840513000','DD/MM/RR HH24:MI:SSXFF'),to_date('13/06/23','DD/MM/RR'));
Insert into BASE_SUSCRIPCIONMODEL (ID,EMAIL,TIMESTAMP,FECHA_CREACION) values (SEQ_SUSCRIPCION.NEXTVAL,'se.salgado@duocuc.cl',to_timestamp('14/06/23 02:38:52,741230000','DD/MM/RR HH24:MI:SSXFF'),to_date('14/06/23','DD/MM/RR'));

/***************************************** INSERT ACCOUNTS_REGION  **********************************************/
Insert into ACCOUNTS_REGION (ID,NOMBRE,FECHA_CREACION) values (SEQ_REGION.NEXTVAL,'Metropolitana',to_timestamp('09/06/23 04:10:56,170522000','DD/MM/RR HH24:MI:SSXFF'));
Insert into ACCOUNTS_REGION (ID,NOMBRE,FECHA_CREACION) values (SEQ_REGION.NEXTVAL,'Valparaiso',to_timestamp('09/06/23 04:11:01,612822000','DD/MM/RR HH24:MI:SSXFF'));

/***************************************** INSERT ACCOUNTS_COMUNA  **********************************************/
Insert into ACCOUNTS_COMUNA (ID,NOMBRE,REGION_ID,FECHA_CREACION) values (SEQ_COMUNA.NEXTVAL,'La Florida','1',to_timestamp('09/06/23 04:11:12,937693000','DD/MM/RR HH24:MI:SSXFF'));
Insert into ACCOUNTS_COMUNA (ID,NOMBRE,REGION_ID,FECHA_CREACION) values (SEQ_COMUNA.NEXTVAL,'Puente Alto','1',to_timestamp('09/06/23 04:11:19,988891000','DD/MM/RR HH24:MI:SSXFF'));
Insert into ACCOUNTS_COMUNA (ID,NOMBRE,REGION_ID,FECHA_CREACION) values (SEQ_COMUNA.NEXTVAL,'Pirque','1',to_timestamp('09/06/23 04:11:25,782857000','DD/MM/RR HH24:MI:SSXFF'));
Insert into ACCOUNTS_COMUNA (ID,NOMBRE,REGION_ID,FECHA_CREACION) values (SEQ_COMUNA.NEXTVAL,'Vaparaiso','2',to_timestamp('09/06/23 04:11:37,036105000','DD/MM/RR HH24:MI:SSXFF'));
Insert into ACCOUNTS_COMUNA (ID,NOMBRE,REGION_ID,FECHA_CREACION) values (SEQ_COMUNA.NEXTVAL,'Concón','2',to_timestamp('09/06/23 04:11:42,471259000','DD/MM/RR HH24:MI:SSXFF'));

/***************************************** INSERT PROVEEDOR_PROVEEDOR  **********************************************/
Insert into PROVEEDOR_PROVEEDOR (ID,NOMBRE_EMPRESA,RUT_EMPRESA,NOMBRE_CONTACTO,CORREO,TELEFONO,DIRECCION,COMUNA_ID,FECHA_CREACION) values (SEQ_PROVEEDOR.NEXTVAL,'PetMed Supplies','17.418.875-0','Juan Pérez','info@petmedsupplies.cl','+56912345678','Avenida Mascotas 123','2',to_timestamp('10/06/23 02:54:04,377277000','DD/MM/RR HH24:MI:SSXFF'));
Insert into PROVEEDOR_PROVEEDOR (ID,NOMBRE_EMPRESA,RUT_EMPRESA,NOMBRE_CONTACTO,CORREO,TELEFONO,DIRECCION,COMUNA_ID,FECHA_CREACION) values (SEQ_PROVEEDOR.NEXTVAL,'Veterquimica','61.019.980-1','Camilo Vallejos','info@veterquimica.cl','+56912345678','Avenida Mascotas 1245','5',to_timestamp('12/06/23 05:04:35,302858000','DD/MM/RR HH24:MI:SSXFF'));
Insert into PROVEEDOR_PROVEEDOR (ID,NOMBRE_EMPRESA,RUT_EMPRESA,NOMBRE_CONTACTO,CORREO,TELEFONO,DIRECCION,COMUNA_ID,FECHA_CREACION) values (SEQ_PROVEEDOR.NEXTVAL,'Drag Pharma','62.492.290-5','Pedro González','info@dragpharma.cl','+56912345678','Avenida Mascotas 5200','5',to_timestamp('15/06/23 05:15:40,473033000','DD/MM/RR HH24:MI:SSXFF'));
Insert into PROVEEDOR_PROVEEDOR (ID,NOMBRE_EMPRESA,RUT_EMPRESA,NOMBRE_CONTACTO,CORREO,TELEFONO,DIRECCION,COMUNA_ID,FECHA_CREACION) values (SEQ_PROVEEDOR.NEXTVAL,'VetCare Products','76.871.207-7','María Gutiérrez','ventas@vetcareproducts.cl','+56912345678','Calle Veterinaria 456','4',to_timestamp('15/06/23 23:52:11,478602000','DD/MM/RR HH24:MI:SSXFF'));
Insert into PROVEEDOR_PROVEEDOR (ID,NOMBRE_EMPRESA,RUT_EMPRESA,NOMBRE_CONTACTO,CORREO,TELEFONO,DIRECCION,COMUNA_ID,FECHA_CREACION) values (SEQ_PROVEEDOR.NEXTVAL,'AnimalPharma Chile','32.622.685-8','Andrés Rodríguez','contacto@animalpharmachile.cl','+5691234567','Plaza Veterinaria 789','5',to_timestamp('10/06/23 23:55:35,053837000','DD/MM/RR HH24:MI:SSXFF'));

/***************************************** INSERT SERVICIO_SERVICIO  **********************************************/
Insert into SERVICIO_SERVICIO (ID,NOMBRE,DESCRIPCION,COSTO,FECHA_CREACION) values (SEQ_SERVICIO.NEXTVAL,'Consulta General','La consulta general en una clínica veterinaria ofrece una evaluación completa de la salud de las mascotas. Incluye exámenes físicos, revisiones de historial médico, recomendaciones preventivas','8000',to_timestamp('09/06/23 04:31:36,672493000','DD/MM/RR HH24:MI:SSXFF'));
Insert into SERVICIO_SERVICIO (ID,NOMBRE,DESCRIPCION,COSTO,FECHA_CREACION) values (SEQ_SERVICIO.NEXTVAL,'Vacunación y Desparasitación','Protege a tu mascota contra enfermedades infecciosas y parásitos con nuestro programa completo de vacunación y desparasitación. Mantén a tu mascota sana y protegida.','15000',to_timestamp('12/06/23 05:43:25,174410000','DD/MM/RR HH24:MI:SSXFF'));
Insert into SERVICIO_SERVICIO (ID,NOMBRE,DESCRIPCION,COSTO,FECHA_CREACION) values (SEQ_SERVICIO.NEXTVAL,'Análisis Clínicos','Nuestro laboratorio veterinario ofrece una amplia gama de análisis clínicos, incluyendo pruebas de sangre, orina y heces, para diagnosticar enfermedades y monitorear la salud de tu mascota.','15000',to_timestamp('12/06/23 05:41:12,277111000','DD/MM/RR HH24:MI:SSXFF'));
Insert into SERVICIO_SERVICIO (ID,NOMBRE,DESCRIPCION,COSTO,FECHA_CREACION) values (SEQ_SERVICIO.NEXTVAL,'Cirugía General','Realizamos una variedad de procedimientos quirúrgicos, desde esterilizaciones hasta extracciones dentales, con un enfoque en la seguridad y la comodidad de tu mascota.','30000',to_timestamp('12/06/23 05:43:06,198471000','DD/MM/RR HH24:MI:SSXFF'));
Insert into SERVICIO_SERVICIO (ID,NOMBRE,DESCRIPCION,COSTO,FECHA_CREACION) values (SEQ_SERVICIO.NEXTVAL,'Consulta Veterinaria','Evaluación exhaustiva de la salud de tu mascota, incluyendo revisión física, diagnóstico y recomendaciones de tratamiento. Cuidamos de la salud y el bienestar de tu mascota.','12000',to_timestamp('12/06/23 05:52:55,918181000','DD/MM/RR HH24:MI:SSXFF'));
Insert into SERVICIO_SERVICIO (ID,NOMBRE,DESCRIPCION,COSTO,FECHA_CREACION) values (SEQ_SERVICIO.NEXTVAL,'Odontología Veterinaria','Nuestro servicio dental ofrece limpieza dental profesional, extracciones, tratamiento de enfermedades periodontales y asesoramiento en cuidado oral, asegurando una salud bucal óptima para mascotas y p','15000',to_timestamp('09/06/23 04:32:46,552518000','DD/MM/RR HH24:MI:SSXFF'));
Insert into SERVICIO_SERVICIO (ID,NOMBRE,DESCRIPCION,COSTO,FECHA_CREACION) values (SEQ_SERVICIO.NEXTVAL,'Vacunación','Ofrecemos un servicio de vacunación completo para perros y gatos, siguiendo los protocolos recomendados por los organismos de salud animal. Protegemos a las mascotas contra enfermedades comunes como','8000',to_timestamp('09/06/23 04:33:41,498389000','DD/MM/RR HH24:MI:SSXFF'));
Insert into SERVICIO_SERVICIO (ID,NOMBRE,DESCRIPCION,COSTO,FECHA_CREACION) values (SEQ_SERVICIO.NEXTVAL,'Hospitalización y Cuidados Intensivos','Contamos con instalaciones de hospitalización y un equipo médico experimentado para brindar atención especializada a mascotas que requieren cuidados intensivos o recuperación después de cirugías.','50000',to_timestamp('13/06/23 23:24:29,576873000','DD/MM/RR HH24:MI:SSXFF'));

/***************************************** INSERT PACIENTE_GENERO  **********************************************/
Insert into PACIENTE_GENERO (ID,NOMBRE,FECHA_CREACION) values (SEQ_GENERO.NEXTVAL,'Macho',to_timestamp('09/06/23 04:13:41,538261000','DD/MM/RR HH24:MI:SSXFF'));
Insert into PACIENTE_GENERO (ID,NOMBRE,FECHA_CREACION) values (SEQ_GENERO.NEXTVAL,'Hembra',to_timestamp('09/06/23 04:13:45,123352000','DD/MM/RR HH24:MI:SSXFF'));

/***************************************** INSERT PACIENTE_ESPECIE  **********************************************/
Insert into PACIENTE_ESPECIE (ID,NOMBRE,FECHA_CREACION) values (SEQ_ESPECIE.NEXTVAL,'Perro',to_timestamp('09/06/23 04:13:23,117416000','DD/MM/RR HH24:MI:SSXFF'));
Insert into PACIENTE_ESPECIE (ID,NOMBRE,FECHA_CREACION) values (SEQ_ESPECIE.NEXTVAL,'Gato',to_timestamp('09/06/23 04:13:26,742235000','DD/MM/RR HH24:MI:SSXFF'));
Insert into PACIENTE_ESPECIE (ID,NOMBRE,FECHA_CREACION) values (SEQ_ESPECIE.NEXTVAL,'Hamster',to_timestamp('09/06/23 04:13:32,611632000','DD/MM/RR HH24:MI:SSXFF'));
Insert into PACIENTE_ESPECIE (ID,NOMBRE,FECHA_CREACION) values (SEQ_ESPECIE.NEXTVAL,'Otra',to_timestamp('09/06/23 05:13:32,611632000','DD/MM/RR HH24:MI:SSXFF'));

/***************************************** INSERT INVENTARIO_CATEGORIA  **********************************************/
Insert into INVENTARIO_CATEGORIA (ID,NOMBRE,FECHA_CREACION) values (SEQ_CATEGORIA.NEXTVAL,'Alimento',to_timestamp('09/06/23 04:12:51,549649000','DD/MM/RR HH24:MI:SSXFF'));
Insert into INVENTARIO_CATEGORIA (ID,NOMBRE,FECHA_CREACION) values (SEQ_CATEGORIA.NEXTVAL,'Medicamento',to_timestamp('09/06/23 04:12:58,014791000','DD/MM/RR HH24:MI:SSXFF'));
Insert into INVENTARIO_CATEGORIA (ID,NOMBRE,FECHA_CREACION) values (SEQ_CATEGORIA.NEXTVAL,'Vacuna',to_timestamp('09/06/23 04:13:05,138656000','DD/MM/RR HH24:MI:SSXFF'));
Insert into INVENTARIO_CATEGORIA (ID,NOMBRE,FECHA_CREACION) values (SEQ_CATEGORIA.NEXTVAL,'Desparasitante',to_timestamp('09/06/23 04:13:10,035549000','DD/MM/RR HH24:MI:SSXFF'));

/***************************************** INSERT INVENTARIO_PRODUCTO  **********************************************/
Insert into INVENTARIO_PRODUCTO (ID,NOMBRE,DESCRIPCION,CANTIDAD,STOCK_MINIMO,PRECIO_VENTA,PRECIO_COMPRA,IMAGEN,FECHA_CREACION,CATEGORIA_ID,PROVEEDOR_ID) values (SEQ_PRODUCTO.NEXTVAL,'Frontline Plus','Un antiparasitario tópico que previene las pulgas y garrapatas en perros y gatos.','20','10','10990','5990','productos/producto1.png',to_timestamp('12/06/23 05:43:53,857764000','DD/MM/RR HH24:MI:SSXFF'),'4','1');
Insert into INVENTARIO_PRODUCTO (ID,NOMBRE,DESCRIPCION,CANTIDAD,STOCK_MINIMO,PRECIO_VENTA,PRECIO_COMPRA,IMAGEN,FECHA_CREACION,CATEGORIA_ID,PROVEEDOR_ID) values (SEQ_PRODUCTO.NEXTVAL,'Heartgard Plus','Un medicamento para la prevención de la enfermedad del gusano del corazón en perros.','10','5','10900','5800','productos/producto2.png',to_timestamp('12/06/23 01:14:22,398471000','DD/MM/RR HH24:MI:SSXFF'),'2','2');
Insert into INVENTARIO_PRODUCTO (ID,NOMBRE,DESCRIPCION,CANTIDAD,STOCK_MINIMO,PRECIO_VENTA,PRECIO_COMPRA,IMAGEN,FECHA_CREACION,CATEGORIA_ID,PROVEEDOR_ID) values (SEQ_PRODUCTO.NEXTVAL,'Royal Canin Veterinary Diet','Una línea de alimentos terapéuticos formulados para abordar necesidades específicas de salud en perros y gatos, como problemas digestivos, alergias o enfermedades renales.','10','6','24990','18990','productos/producto3.png',to_timestamp('11/06/23 01:17:09,710854000','DD/MM/RR HH24:MI:SSXFF'),'1','3');
Insert into INVENTARIO_PRODUCTO (ID,NOMBRE,DESCRIPCION,CANTIDAD,STOCK_MINIMO,PRECIO_VENTA,PRECIO_COMPRA,IMAGEN,FECHA_CREACION,CATEGORIA_ID,PROVEEDOR_ID) values (SEQ_PRODUCTO.NEXTVAL,'Rimadyl','Un medicamento antiinflamatorio no esteroideo (AINE) utilizado para aliviar el dolor en perros, especialmente en casos de artritis.','10','5','20990','18000','productos/producto4.png',to_timestamp('11/06/23 01:19:24,528628000','DD/MM/RR HH24:MI:SSXFF'),'2','4');

/***************************************** INSERT ACCOUNTS_USER  **********************************************/
Insert into ACCOUNTS_USER (ID,PASSWORD,LAST_LOGIN,IS_SUPERUSER,TIPO_USUARIO,USERNAME,RUT,FIRST_NAME,LAST_NAME,EMAIL,DIRECCION,TELEFONO,IS_STAFF,IS_ACTIVE,DATE_JOINED,IMAGE,COMUNA_ID) values (SEQ_USER.NEXTVAL,'pbkdf2_sha256$600000$xNKDbH3XywyJbqpOcu2ex8$CeQF9l/ntRJcgXDQyURtBKWOH984QGOJnFZfb5lHQJM=',to_timestamp('26/06/23 04:10:27,589876000','DD/MM/RR HH24:MI:SSXFF'),'1','administrador','UserAdministrador','11.879.442-7','Administrador','Clinica','django.veterinaria.el.valle@gmail.com','Del empresario 3045','+56996916835','1','1',to_timestamp('09/06/23 04:04:14,761237000','DD/MM/RR HH24:MI:SSXFF'),'user_images\user_1.png','2');
Insert into ACCOUNTS_USER (ID,PASSWORD,LAST_LOGIN,IS_SUPERUSER,TIPO_USUARIO,USERNAME,RUT,FIRST_NAME,LAST_NAME,EMAIL,DIRECCION,TELEFONO,IS_STAFF,IS_ACTIVE,DATE_JOINED,IMAGE,COMUNA_ID) values (SEQ_USER.NEXTVAL,'pbkdf2_sha256$600000$rjMMRPlReT8Ub34BDE8ZZ2$jokzzdDHhPifxkHrxpu84KGfHfuVVegR3kQV05U83uU=',to_timestamp('26/06/23 06:09:18,820593000','DD/MM/RR HH24:MI:SSXFF'),'0','veterinario','User1','24.881.275-3','Usuario','Veterinario 1','marcopezoa.apr@gmail.com','Ernesto Alvear #3214','+56912345678','0','1',to_timestamp('07/06/23 03:49:59,600565000','DD/MM/RR HH24:MI:SSXFF'),'user_images\user_2.png','2');
Insert into ACCOUNTS_USER (ID,PASSWORD,LAST_LOGIN,IS_SUPERUSER,TIPO_USUARIO,USERNAME,RUT,FIRST_NAME,LAST_NAME,EMAIL,DIRECCION,TELEFONO,IS_STAFF,IS_ACTIVE,DATE_JOINED,IMAGE,COMUNA_ID) values (SEQ_USER.NEXTVAL,'pbkdf2_sha256$600000$xNKDbH3XywyJbqpOcu2ex8$CeQF9l/ntRJcgXDQyURtBKWOH984QGOJnFZfb5lHQJM=',null,'0','veterinario','User2','7.844.213-1','Usuario','Veterinario 2','veterinario2@gmail.com','Ernesto Alvear #3214','+56912345678','0','1',to_timestamp('08/06/23 03:49:59,600565000','DD/MM/RR HH24:MI:SSXFF'),'user_images\user_3.png','3');
Insert into ACCOUNTS_USER (ID,PASSWORD,LAST_LOGIN,IS_SUPERUSER,TIPO_USUARIO,USERNAME,RUT,FIRST_NAME,LAST_NAME,EMAIL,DIRECCION,TELEFONO,IS_STAFF,IS_ACTIVE,DATE_JOINED,IMAGE,COMUNA_ID) values (SEQ_USER.NEXTVAL,'pbkdf2_sha256$600000$8m5m1E06rzoQJPM7yGcIUP$z29iYdgV9uQbyQbbng2beU2yxtC9t2UZVrc28xfpiaE=',to_timestamp('26/06/23 06:09:18,820593000','DD/MM/RR HH24:MI:SSXFF'),'0','recepcionista','User3','8.240.453-8','Usuario','Recepcionista 1','zeldapezoa2018@gmail.com','Ernesto Alvear #3214','+56912345678','0','1',to_timestamp('09/06/23 03:49:59,600565000','DD/MM/RR HH24:MI:SSXFF'),'user_images\user_4.png','4');
Insert into ACCOUNTS_USER (ID,PASSWORD,LAST_LOGIN,IS_SUPERUSER,TIPO_USUARIO,USERNAME,RUT,FIRST_NAME,LAST_NAME,EMAIL,DIRECCION,TELEFONO,IS_STAFF,IS_ACTIVE,DATE_JOINED,IMAGE,COMUNA_ID) values (SEQ_USER.NEXTVAL,'pbkdf2_sha256$600000$xNKDbH3XywyJbqpOcu2ex8$CeQF9l/ntRJcgXDQyURtBKWOH984QGOJnFZfb5lHQJM=',null,'0','recepcionista','User4','9.192.903-1','Usuario','Recepcionista 2','recepcionista2@gmail.com','Ernesto Alvear #3214','+56912345678','0','1',to_timestamp('10/06/23 03:49:59,600565000','DD/MM/RR HH24:MI:SSXFF'),'user_images\user_5.png','5');
Insert into ACCOUNTS_USER (ID,PASSWORD,LAST_LOGIN,IS_SUPERUSER,TIPO_USUARIO,USERNAME,RUT,FIRST_NAME,LAST_NAME,EMAIL,DIRECCION,TELEFONO,IS_STAFF,IS_ACTIVE,DATE_JOINED,IMAGE,COMUNA_ID) values (SEQ_USER.NEXTVAL,'pbkdf2_sha256$600000$GN9hkNDK5BkgWdRrVXF0JV$mB26sxmaLBeQjW/1U+do6N7uyA3HY8fjEAf4VbLxNh0=',to_timestamp('26/06/23 06:09:18,820593000','DD/MM/RR HH24:MI:SSXFF'),'0','cliente','User5','14.479.215-7','Usuario','Cliente 1','marcopezoa2014@gmail.com','Ernesto Alvear #3214','+56912345678','0','1',to_timestamp('09/06/23 03:49:59,600565000','DD/MM/RR HH24:MI:SSXFF'),'user_images\user_6.png','1');
Insert into ACCOUNTS_USER (ID,PASSWORD,LAST_LOGIN,IS_SUPERUSER,TIPO_USUARIO,USERNAME,RUT,FIRST_NAME,LAST_NAME,EMAIL,DIRECCION,TELEFONO,IS_STAFF,IS_ACTIVE,DATE_JOINED,IMAGE,COMUNA_ID) values (SEQ_USER.NEXTVAL,'pbkdf2_sha256$600000$xNKDbH3XywyJbqpOcu2ex8$CeQF9l/ntRJcgXDQyURtBKWOH984QGOJnFZfb5lHQJM=',null,'0','cliente','User6','7.908.521-9','Usuario','Cliente 2','cliente2@gmail.com','Ernesto Alvear #3214','+56912345678','0','1',to_timestamp('11/06/23 03:49:59,600565000','DD/MM/RR HH24:MI:SSXFF'),'user_images\user_7.jpg','2');

/***************************************** INSERT ACCOUNTS_USER_GROUPS  **********************************************/
Insert into ACCOUNTS_USER_GROUPS (ID,USER_ID,GROUP_ID) values (SEQ_USER_GROUPS.NEXTVAL,'1','1');
Insert into ACCOUNTS_USER_GROUPS (ID,USER_ID,GROUP_ID) values (SEQ_USER_GROUPS.NEXTVAL,'2','3');
Insert into ACCOUNTS_USER_GROUPS (ID,USER_ID,GROUP_ID) values (SEQ_USER_GROUPS.NEXTVAL,'3','3');
Insert into ACCOUNTS_USER_GROUPS (ID,USER_ID,GROUP_ID) values (SEQ_USER_GROUPS.NEXTVAL,'4','2');
Insert into ACCOUNTS_USER_GROUPS (ID,USER_ID,GROUP_ID) values (SEQ_USER_GROUPS.NEXTVAL,'5','2');
Insert into ACCOUNTS_USER_GROUPS (ID,USER_ID,GROUP_ID) values (SEQ_USER_GROUPS.NEXTVAL,'6','4');
Insert into ACCOUNTS_USER_GROUPS (ID,USER_ID,GROUP_ID) values (SEQ_USER_GROUPS.NEXTVAL,'7','4');

/***************************************** INSERT PACIENTE_PACIENTE  **********************************************/
Insert into PACIENTE_PACIENTE (ID,FECHA_NAC,NOMBRE,EDAD,RAZA,COLOR,NRO_CHIP,FALLECIDO,EXTRAVIADO,ACTIVO,FOTO,DATE_JOINED,"DUEÑO_ID",ESPECIE_ID,GENERO_ID,FECHA_CREACION) values (SEQ_PACIENTE.NEXTVAL,to_date('01/06/15','DD/MM/RR'),'Onix','9','Chapsui','Blanco','CHP123456789','0','0','1','pacientes/mascota1.png',to_timestamp('15/06/23 03:47:27,811710000','DD/MM/RR HH24:MI:SSXFF'),'6','1','1',to_timestamp('15/06/23 03:47:17,694097000','DD/MM/RR HH24:MI:SSXFF')); 
Insert into PACIENTE_PACIENTE (ID,FECHA_NAC,NOMBRE,EDAD,RAZA,COLOR,NRO_CHIP,FALLECIDO,EXTRAVIADO,ACTIVO,FOTO,DATE_JOINED,"DUEÑO_ID",ESPECIE_ID,GENERO_ID,FECHA_CREACION) values (SEQ_PACIENTE.NEXTVAL,to_date('20/03/18','DD/MM/RR'),'Deisy','9','Puddle','Negro','CHP963214568','0','0','1','pacientes/mascota2.png',to_timestamp('15/06/23 03:47:27,811710000','DD/MM/RR HH24:MI:SSXFF'),'7','1','2',to_timestamp('16/06/23 03:47:17,694097000','DD/MM/RR HH24:MI:SSXFF')); 
Insert into PACIENTE_PACIENTE (ID,FECHA_NAC,NOMBRE,EDAD,RAZA,COLOR,NRO_CHIP,FALLECIDO,EXTRAVIADO,ACTIVO,FOTO,DATE_JOINED,"DUEÑO_ID",ESPECIE_ID,GENERO_ID,FECHA_CREACION) values (SEQ_PACIENTE.NEXTVAL,to_date('18/10/14','DD/MM/RR'),'Pelusa','9','Angora','Gris','CHP200021225','0','0','1','pacientes/mascota3.png',to_timestamp('15/06/23 03:47:27,811710000','DD/MM/RR HH24:MI:SSXFF'),'6','2','2',to_timestamp('17/06/23 03:47:17,694097000','DD/MM/RR HH24:MI:SSXFF')); 

/***************************************** INSERT CITA_CITA  **********************************************/
Insert into CITA_CITA (ID,FECHA_CITA,HORARIO,PACIENTE_ID,VETERINARIO_ID,FECHA_CREACION) values (SEQ_CITA.NEXTVAL,to_date('01/06/23','DD/MM/RR'),'1','1','2',to_timestamp('31/05/23 04:16:05,092089000','DD/MM/RR HH24:MI:SSXFF'));
Insert into CITA_CITA (ID,FECHA_CITA,HORARIO,PACIENTE_ID,VETERINARIO_ID,FECHA_CREACION) values (SEQ_CITA.NEXTVAL,to_date('02/06/23','DD/MM/RR'),'2','2','3',to_timestamp('01/06/23 04:16:05,092089000','DD/MM/RR HH24:MI:SSXFF'));
Insert into CITA_CITA (ID,FECHA_CITA,HORARIO,PACIENTE_ID,VETERINARIO_ID,FECHA_CREACION) values (SEQ_CITA.NEXTVAL,to_date('06/06/23','DD/MM/RR'),'3','3','2',to_timestamp('05/06/23 04:16:05,092089000','DD/MM/RR HH24:MI:SSXFF'));
Insert into CITA_CITA (ID,FECHA_CITA,HORARIO,PACIENTE_ID,VETERINARIO_ID,FECHA_CREACION) values (SEQ_CITA.NEXTVAL,to_date('13/06/23','DD/MM/RR'),'4','1','3',to_timestamp('12/06/23 04:16:05,092089000','DD/MM/RR HH24:MI:SSXFF'));

/***************************************** INSERT CONSULTA_CONSULTAMEDICA  **********************************************/
Insert into CONSULTA_CONSULTAMEDICA (ID,FECHA_CONSULTA,PESO,TEMPERATURA,MOTIVO,DIAGNOSTICO,TRATAMIENTO,OBSERVACIONES,ARCHIVOS_PACIENTE,HORARIO_CONSULTA_ID,PACIENTE_ID,SERVICIO_ID,VETERINARIO_ID,FECHA_CREACION,ALTURA,IMC) values (SEQ_CONSULTA.NEXTVAL,to_date('01/06/23','DD/MM/RR'),'6,4','37,5','Pérdida de peso y sed excesiva.','Diabetes mellitus.','Insulina administrada por vía subcutánea, dieta especializada y monitoreo regular de los niveles de glucosa en sangre.','Educar al propietario sobre la administración de insulina y la importancia de mantener una dieta adecuada. Realizar seguimiento para evaluar la regulación de los niveles de glucosa.','documents/2023-05-01_Onix.pdf','1','1','1','2',to_timestamp('01/06/23 04:46:02,610207000','DD/MM/RR HH24:MI:SSXFF'),'20,5','10');
Insert into CONSULTA_CONSULTAMEDICA (ID,FECHA_CONSULTA,PESO,TEMPERATURA,MOTIVO,DIAGNOSTICO,TRATAMIENTO,OBSERVACIONES,ARCHIVOS_PACIENTE,HORARIO_CONSULTA_ID,PACIENTE_ID,SERVICIO_ID,VETERINARIO_ID,FECHA_CREACION,ALTURA,IMC) values (SEQ_CONSULTA.NEXTVAL,to_date('02/06/23','DD/MM/RR'),'6,4','37,5','Pérdida de apetito y letargo.','Infección gastrointestinal.','Antibióticos y medicamentos para aliviar los síntomas gastrointestinales. Dieta especial de alimentos suaves y fácilmente digeribles.','Monitorizar la ingesta de alimentos y la actividad diaria. Programar una cita de seguimiento en una semana.','documents/2023-05-01_Deisy.pdf','2','2','5','3',to_timestamp('02/06/23 04:46:02,610207000','DD/MM/RR HH24:MI:SSXFF'),'20,5','10');
Insert into CONSULTA_CONSULTAMEDICA (ID,FECHA_CONSULTA,PESO,TEMPERATURA,MOTIVO,DIAGNOSTICO,TRATAMIENTO,OBSERVACIONES,ARCHIVOS_PACIENTE,HORARIO_CONSULTA_ID,PACIENTE_ID,SERVICIO_ID,VETERINARIO_ID,FECHA_CREACION,ALTURA,IMC) values (SEQ_CONSULTA.NEXTVAL,to_date('06/06/23','DD/MM/RR'),'5,4','38,4','Cojera y dolor en la pata trasera.','Lesión en la articulación.','Reposo, medicamentos antiinflamatorios y fisioterapia. Se recomienda limitar el ejercicio.','Evitar actividades que puedan agravar la lesión. Proporcionar un ambiente cómodo y seguro para la mascota.','documents/2023-05-03_Onix.pdf','3','3','2','2',to_timestamp('06/06/23 04:46:02,610207000','DD/MM/RR HH24:MI:SSXFF'),'18,2','10');
Insert into CONSULTA_CONSULTAMEDICA (ID,FECHA_CONSULTA,PESO,TEMPERATURA,MOTIVO,DIAGNOSTICO,TRATAMIENTO,OBSERVACIONES,ARCHIVOS_PACIENTE,HORARIO_CONSULTA_ID,PACIENTE_ID,SERVICIO_ID,VETERINARIO_ID,FECHA_CREACION,ALTURA,IMC) values (SEQ_CONSULTA.NEXTVAL,to_date('13/06/23','DD/MM/RR'),'11,5','36,3','Tos persistente y dificultad para respirar.','Infección respiratoria.','Antibióticos y medicamentos para aliviar la tos. Se recomienda mantener a la mascota en un ambiente cálido y sin corrientes de aire.','Controlar los síntomas respiratorios y programar una radiografía de seguimiento para evaluar la mejoría.',null,'4','1','1','3',to_timestamp('13/06/23 04:46:02,610207000','DD/MM/RR HH24:MI:SSXFF'),'25,5','10');

/***************************************** INSERT CONSULTA_DESPARASITACION  **********************************************/
Insert into CONSULTA_DESPARASITACION (ID,NOMBRE,CONSULTA_ID,FECHA) values (SEQ_DESPARASITACION.NEXTVAL,'Brontal','1',to_date('01/06/23','DD/MM/RR'));
Insert into CONSULTA_DESPARASITACION (ID,NOMBRE,CONSULTA_ID,FECHA) values (SEQ_DESPARASITACION.NEXTVAL,'Brontal','3',to_date('06/06/23','DD/MM/RR'));

/***************************************** INSERT CONSULTA_VACUNACION  **********************************************/
Insert into CONSULTA_VACUNACION (ID,NOMBRE,CONSULTA_ID,FECHA) values (SEQ_VACUNACION.NEXTVAL,'Sextuple','1',to_date('01/06/23','DD/MM/RR'));
Insert into CONSULTA_VACUNACION (ID,NOMBRE,CONSULTA_ID,FECHA) values (SEQ_VACUNACION.NEXTVAL,'Octuple','3',to_date('06/06/23','DD/MM/RR'));


/***************************************** CONFIRMACION  **********************************************/

COMMIT;

/***************************************** CONSULTA DE TABLAS  **********************************************/
SELECT * FROM AUTH_GROUP;
SELECT * FROM BASE_CONTACTOMODEL;
SELECT * FROM BASE_SUSCRIPCIONMODEL;
SELECT * FROM ACCOUNTS_REGION;
SELECT * FROM ACCOUNTS_COMUNA;
SELECT * FROM PROVEEDOR_PROVEEDOR;
SELECT * FROM SERVICIO_SERVICIO;
SELECT * FROM PACIENTE_GENERO;
SELECT * FROM PACIENTE_ESPECIE;
SELECT * FROM INVENTARIO_CATEGORIA;
SELECT * FROM INVENTARIO_PRODUCTO;
SELECT * FROM INVENTARIO_REGISTROUSOPRODUCTO;
SELECT * FROM ACCOUNTS_USER;
SELECT * FROM PACIENTE_PACIENTE;
SELECT * FROM CITA_CITA;
SELECT * FROM CONSULTA_CONSULTAMEDICA;
SELECT * FROM CONSULTA_DESPARASITACION;
SELECT * FROM CONSULTA_VACUNACION;
SELECT * FROM AUTH_GROUP_PERMISSIONS;
SELECT * FROM AUTH_PERMISSION;




