/************ Prueba        **********************/
DELETE FROM SERVICIOS;

/************ Prueba        **********************/
DELETE FROM SERVICIO_SERVICIO WHERE COSTO BETWEEN 8000 AND 15000;

/************ Prueba        **********************/
CREATE TABLE historial_historial_medico (
  id NUMBER,
  nombre_paciente VARCHAR2(100),
  fecha DATE,
  diagnostico VARCHAR2(200),
  -- Agrega aquí más columnas según tus necesidades
  CONSTRAINT pk_historial_medico PRIMARY KEY (id)
);

DROP SECUENCE SEQ_HISTORIAL;

CREATE SEQUENCE SEQ_HISTORIAL START WITH 1 INCREMENT BY 1;

INSERT INTO historial_historial_medico (id,nombre_paciente, fecha, diagnostico)
SELECT SEQ_HISTORIAL.NEXTVAL, p.nombre, c.fecha_consulta, c.diagnostico
FROM PACIENTE_PACIENTE p
JOIN CONSULTA_CONSULTAMEDICA c ON p.id = c.paciente_id;

/************ Prueba        **********************/
SELECT p.id, p.Nombre, p.especie_id, p.Raza
FROM PACIENTE_PACIENTE p
LEFT JOIN CONSULTA_CONSULTAMEDICA c ON p.id = c.paciente_id
WHERE c.id IS NULL

SELECT * FROM PACIENTE_PACIENTE
SELECT * FROM consulta_consultamedica

/************ Prueba        **********************/
DELETE FROM consulta_consultamedica
WHERE id BETWEEN 10 AND 20;

ROLLBACK;

SELECT * FROM consulta_consultamedica ORDER BY ID

/************ Prueba        **********************/
UPDATE servicio_servicio
SET COSTO = 50000
WHERE id = 1;

select * from servicio_servicio;

/************ Prueba        **********************/
UPDATE accounts_user
SET FIRST_NAME = 'Sebastian'
WHERE id = 5;

UPDATE accounts_user
SET FIRST_NAME = 'Marco'
WHERE id = 6;

UPDATE accounts_user
SET FIRST_NAME = 'Julio'
WHERE id = 7;

SELECT * FROM accounts_user

/************ Prueba        **********************/



/************ Prueba        **********************/