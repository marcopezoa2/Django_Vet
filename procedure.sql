/****************************************************************************************************************************/
-- Crear Procedimientos Almacenados--
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

/****************************************************************************************************************************/
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
/****************************************************************************************************************************/








/*
CREATE OR REPLACE PROCEDURE SP_CONSUMIR_PRODUCTO(
    p_producto_id IN NUMBER,
    p_cantidad_utilizada IN NUMBER
) IS
    l_stock_minimo INVENTARIO_PRODUCTO.stock_minimo%TYPE;
    l_cantidad INVENTARIO_PRODUCTO.cantidad%TYPE;
BEGIN
    -- Verificar si el producto existe
    SELECT stock_minimo, cantidad INTO l_stock_minimo, l_cantidad
    FROM INVENTARIO_PRODUCTO
    WHERE id = p_producto_id;

    IF l_stock_minimo IS NULL THEN
        -- El producto no existe, generar un error
        RAISE_APPLICATION_ERROR(-20001, 'El producto seleccionado no existe.');
    END IF;

    -- Verificar si la cantidad utilizada es válida
    IF p_cantidad_utilizada <= 0 THEN
        -- La cantidad utilizada debe ser mayor que 0, generar un error
        RAISE_APPLICATION_ERROR(-20002, 'La cantidad utilizada debe ser mayor que 0.');
    END IF;

    IF p_cantidad_utilizada > l_cantidad THEN
        -- La cantidad utilizada es mayor que la cantidad disponible en el inventario, generar un error
        RAISE_APPLICATION_ERROR(-20003, 'La cantidad utilizada es mayor que la cantidad disponible en el inventario.');
    END IF;

    -- Realizar el consumo de producto
    UPDATE INVENTARIO_PRODUCTO
    SET cantidad = cantidad - p_cantidad_utilizada
    WHERE id = p_producto_id;

    -- Registrar el uso del producto
    INSERT INTO INVENTARIO_REGISTROUSOPRODUCTO (producto_utilizado_id, cantidad_utilizada)
    VALUES (p_producto_id, p_cantidad_utilizada);

    -- Verificar si el producto ha alcanzado o bajado del stock mínimo
    SELECT cantidad INTO l_cantidad
    FROM INVENTARIO_PRODUCTO
    WHERE id = p_producto_id;

    IF l_cantidad <= l_stock_minimo THEN
        -- El producto ha alcanzado o bajado del stock mínimo, mostrar mensaje de advertencia
        DBMS_OUTPUT.PUT_LINE('El producto ' || p_producto_id || ' ha alcanzado o bajado del stock mínimo. Por favor, reponga el producto.');
    ELSE
        -- El consumo se ha registrado correctamente, mostrar mensaje de éxito
        DBMS_OUTPUT.PUT_LINE('Se ha registrado el consumo de ' || p_cantidad_utilizada || ' unidades del producto ' || p_producto_id || '.');
    END IF;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        -- Manejar cualquier error que ocurra
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
        ROLLBACK;
        RAISE;
END;
/




CREATE OR REPLACE PROCEDURE SP_ELIMINAR_PRODUCTO (
    p_producto_id IN NUMBER
) IS
BEGIN
    -- Eliminar el producto de la tabla INVENTARIO_PRODUCTO
    DELETE FROM INVENTARIO_PRODUCTO
    WHERE id = p_producto_id;

    -- Mostrar mensaje de éxito
    DBMS_OUTPUT.PUT_LINE('¡Producto eliminado con éxito!');
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        -- Manejar cualquier error que ocurra
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
        ROLLBACK;
        RAISE;
END;
*/




/*
CREATE OR REPLACE PROCEDURE SP_REALIZAR_RESPALDO_BD AS
BEGIN
  -- Define los parámetros para la exportación
  DECLARE
    v_dumpfile VARCHAR2(100) := 'C:\Users\marco\Desktop\Respaldo_BD_ClinicaVet\respaldoBD_ClinicaVet.dmp';
    v_logfile VARCHAR2(100) := 'C:\Users\marco\Desktop\Respaldo_BD_ClinicaVet\respaldoBD_ClinicaVet_log.log';
  BEGIN
    -- Ejecuta la exportación utilizando Data Pump
    DBMS_DATAPUMP.OPEN('EXPORT', 'FULL', NULL, 'COMPRESS=ALL');
    DBMS_DATAPUMP.ADD_FILE(1, v_dumpfile, NULL);
    DBMS_DATAPUMP.ADD_FILE(2, v_logfile, NULL);
    DBMS_DATAPUMP.METADATA_FILTER('SCHEMA_EXPR', 'IN (''SCHEMA1'', ''SCHEMA2'')');
    DBMS_DATAPUMP.START_JOB(NULL, 'EXPORT', NULL, NULL, 0, 0);
    DBMS_DATAPUMP.WAIT_FOR_JOB(NULL, job_state);
    DBMS_DATAPUMP.DETACH('EXPORT');
  EXCEPTION
    WHEN OTHERS THEN
      -- Maneja cualquier error que ocurra durante la exportación
      DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
      DBMS_DATAPUMP.DETACH('EXPORT');
      RAISE;
  END;
END;
/

*/