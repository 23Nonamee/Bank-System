# Sistema Bancario - SouthPark Bank
**Evaluación Sumativa N°3: Persistencia, Seguridad y Consumo de Servicios en Python**  
**Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)  
**Institución:** INACAP - Sede Puente Alto  

---

## 1. Integrantes y Negocio

- **Negocio:** Banco (SouthPark Bank).
- **Equipo:** 
- **Integrante:** Isaias Arancibia.
- **RUT:** 21.873.976-8.
- **Indicador Económico Externo:** UF (Unidad de Fomento) y Dólar Observado (USD) consumidos en tiempo real desde la API pública `https://mindicador.cl`.

---

## 2. Cómo Instalar y Ejecutar Paso a Paso

El software está diseñado para ejecutarse en cualquier computador que disponga de Python 3.10 o superior, sin configuraciones complejas y creando automáticamente su base de datos local SQLite.

### 2.1. Clonación e Instalación de Dependencias

1. **Abrir una terminal o consola** y ubicarse en el directorio del proyecto:
   ```bash
   cd Bank-System
   ```

2. **(Opcional pero recomendado) Crear y activar un entorno virtual:**
   - En Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - En Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instalar los paquetes requeridos:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Instala `requests>=2.31.0` necesario para el consumo de la API de indicadores económicos).*

4. **Ejecutar el programa:**
   ```bash
   python main.py
   ```
   *(o `python3 main.py` según la configuración de su sistema).*

---

### 2.2. Guía de Ejecución de las Pruebas del Profesor (P01 a P19)

El sistema provee dos mecanismos para comprobar las pruebas:
- **Modo Automatizado:** Seleccionar la opción **`6`** en el menú principal para ejecutar de principio a fin los 19 casos de prueba con verificación de base de datos y generar la tabla resumen de resultados.
- **Modo Interactivo (Manual paso a paso):** A través de las opciones del menú de consola:

| N° | Prueba | Menú y Pasos a Seguir | Dato de Prueba | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| **P01** | El programa se ejecuta | Ejecutar `python main.py` | Iniciar sistema | El programa inicia y muestra el menú principal interactivo. |
| **P02** | Crear: cliente | Opción `1` -> Opción `1` | Nombre: `Luis Pérez`, RUT: `12.345.678-5`, Dirección: `Av. Libertador 123` | El programa confirma que se guardó en SQLite. |
| **P03** | Listar: cliente | Opción `1` -> Opción `2` | Consultar listado | Aparece el registro recién creado con sus datos. |
| **P04** | Modificar: cliente | Opción `1` -> Opción `3` | RUT: `12.345.678-5`, Nueva dirección: `Av. Las Lilas 456`. Listar con opción `2`. | El listado muestra la dirección actualizada. |
| **P05** | Los datos quedan guardados | Salir con `0`, volver a ejecutar `python main.py` y listar (`1` -> `2`) | Reabrir programa | El registro de Luis Pérez sigue en la base de datos `banco.db`. |
| **P06** | Eliminar: cliente | Opción `1` -> Opción `4` | RUT: `12.345.678-5`. Confirmar eliminación y luego listar (`2`). | El registro ya no aparece en el sistema. |
| **P07** | RUT del cliente: dato correcto | Opción `1` -> Opción `1` | RUT: `12.345.678-5` | Lo acepta correctamente según algoritmo Módulo 11. |
| **P08** | RUT del cliente: dato incorrecto | Opción `1` -> Opción `1` | RUT: `12.345.678-9` (DV incorrecto) | Lo rechaza con un mensaje de advertencia y el programa sigue funcionando sin caerse. |
| **P09** | Tipo Cuenta corriente | Opción `2` -> Opción `1` y luego Opción `5` | Cuenta corriente `CC-101`, cupo sobregiro $100.000 | Sin interés a favor; permite sobregiro hasta el cupo asignado. |
| **P10** | Tipo Cuenta de ahorro | Opción `2` -> Opción `2` y luego Opción `5` | Cuenta de ahorro `CA-201`, saldo $500.000, tasa 4% | Gana interés mensual positivo indexado a su saldo. |
| **P11** | Tipo Cuenta vista | Opción `2` -> Opción `3` y luego Opción `5` | Cuenta vista `CV-301`, saldo $80.000 | No gana interés ni permite sobregiro (disponible = saldo). |
| **P12** | Registrar: cartola | Opción `4` -> Opción `1` | Cuenta registrada (ej: `CV-301`), registra Depósito ($50.000), Giro ($20.000) y Cargo ($3.500) | Queda guardado como un solo registro de transacción con sus 3 movimientos. |
| **P13** | Ver el detalle: cartola | Opción `4` -> Opción `2` | Consultar número de cuenta | Se despliega la cartola con todas sus líneas de detalle. |
| **P14** | Regla: Girar más que saldo en cuenta vista | Opción `3` -> Opción `2` | Cuenta vista con saldo $10.000. Girar $15.000 | El giro se bloquea con `SaldoInsuficienteError`; el saldo no cambia y el programa sigue activo. |
| **P15** | Regla: Abrir cuenta a cliente con mora | Opción `1` -> Opción `5` (asignar mora), luego Opción `2` -> Opción `3` | Cliente con mora vigente. Intentar abrirle una cuenta | La apertura se bloquea con `ClienteEnMoraError`; el programa continúa funcionando. |
| **P16** | Precio con la UF del día | Opción `5` -> Opción `1` | Conexión a `https://mindicador.cl/api/uf` | El programa consume el valor real del día y reajusta la tasa/interés de la cuenta de ahorro. |
| **P17** | Sin internet | Opción `5` -> Opción `3` (o desconectar wifi y usar opción `1`) | Desconexión de red / timeout inmediato | El programa avisa que no pudo obtener el valor y NO se cae. |
| **P18** | Opción de menú que no existe | En el menú principal ingresar `99` | Opción `99` | Muestra mensaje `"Opción '99' no es válida"` y regresa al menú. |
| **P19** | Letras donde va un número | Opción `3` -> Opción `1` (Monto depósito) | Ingresar `-1000`, `0` o `abc` | Rechaza la entrada con mensaje explicativo y el programa no se cae. |

---

## 3. Decisiones de Seguridad

### 3.1. Prevención de Inyección SQL (SQL Injection - CWE-89)
La persistencia de datos implementada en la carpeta `dao/` utiliza exclusivamente la librería estándar oficial `sqlite3` aplicando consultas parametrizadas mediante marcadores de posición (`?`).
- **Regla estricta:** Está terminantemente prohibido el uso de concatenación de cadenas (`+`), interpolación de cadenas (`%`) o f-strings (`f"..."`) con datos provistos por el usuario.
- **Transaccionalidad ACID:** En operaciones compuestas (como el registro de una `Transaccion` junto con sus líneas de detalle `Movimiento`), se gestiona la transacción mediante un bloque atómico con `conn.commit()` y `conn.rollback()`.

#### Ejemplo de Código Real del Repositorio ([dao/cliente_dao.py](file:///home/noname/Desktop/projects/Bank-System/dao/cliente_dao.py)):
```python
# SEGURO: La consulta utiliza marcadores posicionales (?) y los valores se pasan como tupla separada.
sql = """
    INSERT INTO clientes (rut, nombre, direccion, is_mora, amount_mora)
    VALUES (?, ?, ?, ?, ?);
"""
cursor.execute(sql, (rut_fmt, cliente.nombre, cliente.direccion, is_mora, amount_mora))
conn.commit()
```

#### Ejemplo de Persistencia Atómica Cabecera-Detalle ([dao/transaccion_dao.py](file:///home/noname/Desktop/projects/Bank-System/dao/transaccion_dao.py)):
```python
try:
    cursor.execute("INSERT INTO transacciones (numero_cuenta, fecha) VALUES (?, ?);", 
                   (transaccion.cuenta.numero_cuenta, fecha_iso))
    transaccion_id = cursor.lastrowid

    for mov in transaccion.detalles:
        cursor.execute("""
            INSERT INTO movimientos (transaccion_id, tipo, monto, descripcion, cuenta_origen, cuenta_destino)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (transaccion_id, mov.tipo.value, mov.monto, mov.descripcion, origen_num, destino_num))

    conn.commit()  # Confirmación atómica de cabecera y detalles
except Exception as ex:
    conn.rollback()  # Reversión completa en caso de cualquier fallo
    raise ex
```

### 3.2. Validación Defensiva de Entradas

El sistema aplica validación en dos capas para garantizar robustez y coherencia de datos:

1. **En la Capa de Modelo (Encapsulamiento en Setters):**
   - **RUT Chileno ([model/rut.py](file:///home/noname/Desktop/projects/Bank-System/model/rut.py)):** El setter `@identificador.setter` aplica el algoritmo oficial Módulo 11 sobre el dígito verificador. Si el dígito es incorrecto o el formato no es válido, levanta `RutInvalidoError`.
   - **Nombre y Dirección ([model/cliente.py](file:///home/noname/Desktop/projects/Bank-System/model/cliente.py)):** Setters `@nombre.setter` y `@direccion.setter` verifican tipo `str`, longitud mínima y eliminan espacios vacíos.
   - **Saldos y Montos ([model/cuenta.py](file:///home/noname/Desktop/projects/Bank-System/model/cuenta.py)):** Setters y métodos `ingresarDinero()` / `retirarDinero()` validan tipo numérico (`int`, `float`) y montos estrictamente positivos (`> 0`).
   - **Reglas Bloqueantes de Negocio:**
     - `SaldoInsuficienteError`: Lanzada si un giro o transferencia supera el saldo disponible real.
     - `ClienteEnMoraError`: Lanzada al intentar retirar fondos con mora activa, o al intentar abrir una cuenta para un cliente con mora vigente mediante `CuentaFactory.crearCuenta()`.

2. **En la Capa de Interfaz y Consola ([main.py](file:///home/noname/Desktop/projects/Bank-System/main.py)):**
   - Funciones auxiliares `leer_monto()`, `leer_rut()` y `leer_texto()` capturan errores de conversión (`ValueError`, `TypeError`), informando al usuario el motivo del rechazo y retornando al menú sin que el proceso termine abruptamente.

---

## 4. Uso de Inteligencia Artificial

Durante el proceso de desarrollo asistido con Inteligencia Artificial, se analizaron diversas recomendaciones técnicas, aplicando criterio profesional para adoptar, modificar o descartar componentes de acuerdo con los requerimientos de seguridad y arquitectura:

### Caso 1: Descarte de Consultas Dinámicas con Formateo de Texto (SQL Injection)
- **Sugerencia de la IA:** Para el método `actualizar` de `ClienteDAO`, la IA propuso concatenar nombres de campos y valores mediante diccionarios y f-strings (`f"UPDATE clientes SET {campo} = '{valor}' WHERE rut = '{rut}'"`), argumentando que permitía actualizar únicamente los campos que hubiesen cambiado.
- **Decisión Técnica:** **DESCARTADO.** Concatenar cadenas directamente en sentencias SQL introduce vulnerabilidades críticas de inyección SQL (CWE-89). Se descartó la sugerencia y se implementó una consulta SQL explícita con marcadores parametrizados `?` que pasa todos los valores como parámetros vinculados del motor SQLite.

### Caso 2: Modificación del Manejo de Excepciones en el Consumo de API
- **Sugerencia de la IA:** En el módulo de consumo de la API de indicadores externos (`mindicador.cl`), la IA sugirió envolver toda la petición en un bloque genérico `try ... except Exception as e: return None`.
- **Decisión Técnica:** **MODIFICADO.** Un bloque `except Exception` genérico viola los principios de manejo seguro de errores (Criterio 3.1.3), ya que silencia errores de red, impide distinguir un timeout de una falta de conectividad y enmascara fallos estructurales en los datos. Se modificó el código para capturar de forma específica `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, `requests.exceptions.HTTPError` y `json.JSONDecodeError`, mapeándolos a excepciones de dominio explícitas (`ApiTimeoutError`, `ApiConexionError`, `ApiIndicadorError`) y manteniendo la aplicación estable.

### Caso 3: Adopción del Patrón de Persistencia Atómica Transacción-Movimientos
- **Sugerencia de la IA:** Implementar la inserción de la cabecera `transacciones` y sus líneas hijas `movimientos` dentro de un único contexto transaccional SQLite controlado por `try ... conn.commit()` y `except ... conn.rollback()`.
- **Decisión Técnica:** **ADOPTADO.** Esta recomendación cumple con el estándar de integridad referencial bancaria (propiedades ACID), asegurando que si ocurre un error al persistir cualquiera de los movimientos (depósito, giro o cargo), no queden registros huérfanos de transacciones sin detalle en la base de datos.
