# 🏛️ Sistema Bancario - SouthPark Bank

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![SQLite3](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-19%2F19%20Pasan-success)
![Frontend](https://img.shields.io/badge/UI-CLI%20%2B%20Web%20GUI-0284c7)
![Seguridad](https://img.shields.io/badge/Seguridad-CWE--89%20%7C%20M%C3%B3dulo%2011-darkgreen)

---

## 1. Integrantes y negocio

- **Negocio asignado:** Banco (**SouthPark Bank**).
- **Equipo:** *(Trabajo Individual)*.
- **Integrante:** Isaias Arancibia.
- **RUT:** 21.873.976-8.
- **Institución:** INACAP - Sede Puente Alto.
- **Carrera:** Ingeniería Informática.
- **Asignatura:** Programación Orientada a Objeto Seguro (TI3V21).
- **Docente:** Michael Arjel.
- **Indicador Económico Externo:** Unidad de Fomento (UF) y Dólar Observado (USD) consumidos en tiempo real mediante la API pública de `https://mindicador.cl`.

---

## 2. Cómo instalar y ejecutar el programa, paso a paso, desde un computador que solo tiene Python

El software está diseñado para ejecutarse de manera autónoma en cualquier computador que disponga de **Python 3.10 o superior**, sin necesidad de instalar motores de bases de datos externos ni software adicional, ya que utiliza la librería nativa `sqlite3` y crea automáticamente su base de datos local `banco.db` al iniciar.

### Paso 1: Clonar o descargar el repositorio
Abrir una terminal (consola de comandos) y ubicarse en la carpeta raíz del proyecto:
```bash
cd Bank-System
```

### Paso 2: (Opcional pero recomendado) Crear y activar un entorno virtual
- En **Linux / macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- En **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### Paso 3: Instalar paquetes requeridos
Instalar la única dependencia externa necesaria para el consumo de la API económica:
```bash
pip install -r requirements.txt
```
*(Instala `requests>=2.31.0`).*

### Paso 4: Ejecutar el programa
Iniciar el lanzador principal ejecutando:
```bash
python main.py
```
*(O `python3 main.py` según la configuración de su sistema).*

### Paso 5: Selección de Modo de Ejecución
Al iniciar, el sistema despliega el selector interactivo:

```text
=================================================================
                SISTEMA BANCARIO - SOUTHPARK BANK
     Asignatura: Programación Orientada a Objeto Seguro
     Equipo: | Integrante: Isaias Arancibia
=================================================================
  Seleccione el modo de ejecución:
  1. Modo Consola (CLI interactivo y Guion de Pruebas Docente)
  2. Modo Interfaz Gráfica (GUI Web en el Navegador)
  0. Salir del sistema
=================================================================
👉 Ingrese su opción [1/2/0]: 
```

- **Opción `1` (Modo Consola - CLI):**  
  Despliega el menú tradicional interactivo por terminal para gestionar clientes, aperturar cuentas, transferir, ver cartolas, consultar divisas y ejecutar la batería de pruebas docentes.
- **Opción `2` (Modo Interfaz Gráfica - Web GUI):**  
  Inicia automáticamente un servidor web local en segundo plano en `http://localhost:8000` y **abre su navegador predeterminado** con la plataforma web multi-rol de SouthPark Bank. Al presionar <kbd>Enter</kbd> en la terminal, el servidor se detiene de forma limpia. *(También puede abrirse directamente haciendo doble clic en `frontend/index.html`)*.

> **Atajos directos por línea de comandos:**  
> - `python main.py --cli` : Ingresa directo al menú de consola.  
> - `python main.py --gui` : Inicia directo el servidor web y abre el navegador.  
> - `python main.py --test` : Ejecuta directamente la batería de pruebas P01 a P19.

---

### 2.1. Perfiles y Usuarios Demo (Multi-Rol para la Web GUI)

En la pantalla de inicio de sesión de la Web GUI se dispone de botones de **acceso rápido con 1 clic** para alternar entre perfiles:

| Perfil | Usuario / RUT | Clave | Funcionalidades Habilitadas |
| :--- | :--- | :---: | :--- |
| **👤 Cliente Titular**<br>*(Isaias Arancibia)* | `cliente`<br>`12.345.678-5` | `123456` | • Saldo real, cupo de sobregiro y disponible total.<br>• Historial de últimos movimientos en cartola.<br>• Transferencias con modal de confirmación antes de debitar.<br>• Calculadora de divisas CLP ↔ USD con tasa oficial en vivo. |
| **💵 Cajero Bancario**<br>*(Juan Morales)* | `cajero`<br>`14.253.647-8` | `123456` | • Ventanilla de depósitos y giros de efectivo en tiempo real.<br>• Bloqueo defensivo por fondos insuficientes (**P14**).<br>• Bloqueo de operaciones a clientes con morosidad (**P15**).<br>• Consulta de saldos y mora de cualquier cuenta. |
| **💼 Ejecutivo de Cuentas**<br>*(Andrea Soto)* | `ejecutivo`<br>`15.364.758-9` | `123456` | • **Apertura de Cuentas (`CuentaFactory`):** Corriente, Ahorro y Vista.<br>• **Regla Bloqueante P15:** Alerta defensiva si el cliente registra mora.<br>• **Alta de Clientes:** Validación de RUT Módulo 11 y dirección mínima. |
| **🛡️ Administrador**<br>*(Carlos Admin)* | `admin`<br>`11.111.111-1` | `123456` | • Acceso irrestricto a todas las vistas del banco.<br>• Métricas globales de fondos, cuentas y clientes.<br>• **Ejecutor Web de Pruebas Docente:** Evalúa las 19 pruebas interactivamente.<br>• **Simulador de Morosidad:** Switch para activar/desactivar mora a cualquier cliente. |

---

### 2.2. Guía de Ejecución de las Pruebas Docente (P01 a P19)

Para verificar el cumplimiento de las 19 pruebas oficiales, seleccione la opción **`6`** en la consola o el botón **"▶️ Ejecutar las 19 Pruebas"** en el panel de Administrador de la Web GUI:

| N° | Caso de Prueba | Entrada de Prueba | Comportamiento del Sistema | Estado |
| :---: | :--- | :--- | :--- | :---: |
| **P01** | El programa se ejecuta | `python main.py` | Despliega selector y menú sin errores de inicio | ✅ CUMPLE |
| **P02** | Crear: cliente | Luis Pérez, 12.345.678-5 | Persistido en tabla `clientes` de SQLite | ✅ CUMPLE |
| **P03** | Listar: cliente | Consulta general | Registro recuperado y mostrado en pantalla | ✅ CUMPLE |
| **P04** | Modificar: cliente | Modificar dirección a Av. Las Lilas 456 | Actualizado en base de datos y confirmado en listado | ✅ CUMPLE |
| **P05** | Los datos quedan guardados | Cierre (`0`) y reapertura del programa | Datos persisten intactos en disco (`banco.db`) | ✅ CUMPLE |
| **P06** | Eliminar: cliente | Borrado por RUT | Registro eliminado permanentemente | ✅ CUMPLE |
| **P07** | RUT correcto | 12.345.678-5 | Aceptado por el algoritmo oficial Módulo 11 | ✅ CUMPLE |
| **P08** | RUT incorrecto | 12.345.678-9 (DV erróneo) | Rechazado con `RutInvalidoError`; no colapsa | ✅ CUMPLE |
| **P09** | Cuenta corriente | CC-1001-9874 (Cupo $300.000) | Sin interés a favor; permite sobregiro | ✅ CUMPLE |
| **P10** | Cuenta de ahorro | CA-2001-4412 (Tasa 4.5%) | Genera interés mensual positivo y reajuste UF | ✅ CUMPLE |
| **P11** | Cuenta vista | CV-3001-7711 (Saldo $80.000) | Disponible estricto; interés = $0 | ✅ CUMPLE |
| **P12** | Registrar cartola | Depósito + Giro + Cargo | Guardado como 1 transacción con 3 movimientos | ✅ CUMPLE |
| **P13** | Ver detalle cartola | Consulta por N° de cuenta | Muestra desglose de las 3 líneas de detalle | ✅ CUMPLE |
| **P14** | Regla: Girar más que saldo | Cuenta vista saldo $10.000, girar $15.000 | Bloqueado con `SaldoInsuficienteError`; saldo intacto | ✅ CUMPLE |
| **P15** | Regla: Abrir cuenta con mora | Cliente con mora vigente ($120.000) | Bloqueado con `ClienteEnMoraError`; no crea cuenta | ✅ CUMPLE |
| **P16** | Precio con UF del día | API `mindicador.cl/api/uf` | Obtiene valor real y reajusta interés | ✅ CUMPLE |
| **P17** | Sin internet | Simulación red caída / timeout | Emite advertencia descriptiva y no colapsa | ✅ CUMPLE |
| **P18** | Opción inexistente | Ingreso de opción `99` | Muestra mensaje y retorna al menú principal | ✅ CUMPLE |
| **P19** | Letras donde va número | Entradas `-1000`, `0`, `abc` | Rechaza valores inválidos y programa sigue activo | ✅ CUMPLE |

**Efectividad Comprobada:** **19 de 19 pruebas cumplidas exitosamente (100.0%)**.

---

## 3. Decisiones de seguridad

### 3.1. Cómo se evita la inyección SQL (SQL Injection - CWE-89)

La persistencia de datos implementada en la capa `dao/` utiliza exclusivamente la librería estándar oficial `sqlite3` aplicando consultas parametrizadas mediante marcadores de posición posicionales (`?`).

- **Regla estricta:** Está terminantemente prohibido el uso de concatenación de cadenas (`+`), interpolación de cadenas (`%`) o f-strings (`f"..."`) con datos provistos por el usuario.
- **Transaccionalidad Atómica (ACID):** En operaciones compuestas (como el registro de una `Transaccion` junto con sus líneas de detalle `Movimiento`), se gestiona la transacción dentro de un bloque atómico protegido por `try ... conn.commit()` y `except ... conn.rollback()`, asegurando que no queden transacciones huérfanas ante cualquier interrupción.

#### Ejemplo de Código Real del Repositorio (`dao/cliente_dao.py`):
```python
# SEGURO: La consulta utiliza marcadores posicionales (?) y los valores se pasan como tupla separada.
sql = """
    INSERT INTO clientes (rut, nombre, direccion, is_mora, amount_mora)
    VALUES (?, ?, ?, ?, ?);
"""
cursor.execute(sql, (rut_fmt, cliente.nombre, cliente.direccion, is_mora, amount_mora))
conn.commit()
```

#### Ejemplo de Persistencia Atómica Cabecera-Detalle (`dao/transaccion_dao.py`):
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

---

### 3.2. Qué entradas se validan (Validación Defensiva)

El sistema aplica validación defensiva en múltiples capas para garantizar la integridad de datos:

1. **RUT Chileno con Algoritmo Módulo 11 (`model/rut.py` y `frontend/app.js`):**  
   El setter `@identificador.setter` descompone el cuerpo y el dígito verificador, aplicando la serie numérica multiplicadora `[2, 3, 4, 5, 6, 7]`. Si el dígito calculado no coincide exactamente con el ingresado (o si el formato es erróneo), levanta inmediatamente `RutInvalidoError`, impidiendo la creación o actualización de clientes con RUTs falsos o erróneos (**P07 y P08**).
2. **Nombres y Direcciones (`model/cliente.py`):**  
   Los setters `@nombre.setter` y `@direccion.setter` verifican tipo de dato `str`, aplican `strip()` para eliminar espacios en blanco y validan longitud mínima (`len >= 2`), superando la prueba **P04** ("cambiar dirección y listar").
3. **Montos y Saldos Bancarios (`model/cuenta.py`):**  
   Los métodos `ingresarDinero()` y `retirarDinero()` validan tipo numérico (`int` o `float`) y montos estrictamente positivos (`monto > 0`). Valores menores o iguales a cero, caracteres alfabéticos o números negativos son rechazados impidiendo la corrupción de saldos (**P19**).
4. **Reglas Bloqueantes de Negocio:**
   - `SaldoInsuficienteError`: Lanzada si un giro excede el saldo real sumado al cupo de sobregiro (**P14**).
   - `ClienteEnMoraError`: Lanzada al intentar aperturar una cuenta para un cliente con mora vigente mediante `CuentaFactory.crearCuenta()` (**P15**), o al intentar efectuar giros con morosidad activa.
5. **Resiliencia de Red y Excepciones Tipadas (`services/indicador_service.py`):**  
   Al consultar la API de `mindicador.cl`, se define un `timeout=5.0` y se capturan de forma explícita `requests.exceptions.Timeout` (`ApiTimeoutError`), `requests.exceptions.ConnectionError` (`ApiConexionError`), `requests.exceptions.HTTPError` y `json.JSONDecodeError` (`ApiIndicadorError`), garantizando que si se interrumpe la conexión a internet, el sistema informe al usuario sin abortar el proceso (**P17**).
6. **Entradas por Consola y Web:**  
   Funciones auxiliares `leer_monto()`, `leer_rut()` y `leer_texto()` en `main.py` capturan errores de conversión (`ValueError`), notificando al usuario y retornando al menú sin colapsar el programa (**P18 y P19**).

---

## 4. Uso de inteligencia artificial

Durante el proceso de desarrollo asistido con Inteligencia Artificial, se analizaron diversas recomendaciones técnicas, aplicando criterio profesional para adoptar, modificar o descartar componentes de acuerdo con los requerimientos de seguridad, persistencia y arquitectura de la rúbrica:

### Caso 1: Descarte de Consultas Dinámicas con Formateo de Texto (SQL Injection)
- **Sugerencia de la IA:** Para el método `actualizar` de `ClienteDAO`, la IA propuso concatenar nombres de campos y valores mediante diccionarios y f-strings (`f"UPDATE clientes SET {campo} = '{valor}' WHERE rut = '{rut}'"`), argumentando que permitía actualizar únicamente los campos que hubiesen cambiado.
- **Decisión Técnica:** **DESCARTADO.** Concatenar cadenas directamente en sentencias SQL introduce vulnerabilidades críticas de inyección SQL (CWE-89). Se descartó la sugerencia y se implementó una consulta SQL explícita con marcadores parametrizados `?` que pasa todos los valores como parámetros vinculados del motor SQLite.

### Caso 2: Modificación del Manejo de Excepciones en el Consumo de API
- **Sugerencia de la IA:** En el módulo de consumo de la API de indicadores externos (`mindicador.cl`), la IA sugirió envolver toda la petición en un bloque genérico `try ... except Exception as e: return None`.
- **Decisión Técnica:** **MODIFICADO.** Un bloque `except Exception` genérico viola los principios de manejo seguro de errores (Criterio 3.1.3), ya que silencia errores de red, impide distinguir un timeout de una falta de conectividad y enmascara fallos estructurales en los datos. Se modificó el código para capturar de forma específica `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, `requests.exceptions.HTTPError` y `json.JSONDecodeError`, mapeándolos a excepciones de dominio explícitas (`ApiTimeoutError`, `ApiConexionError`, `ApiIndicadorError`) y manteniendo la aplicación estable.

### Caso 3: Adopción del Patrón de Persistencia Atómica Transacción-Movimientos
- **Sugerencia de la IA:** Implementar la inserción de la cabecera `transacciones` y sus líneas hijas `movimientos` dentro de un único contexto transaccional SQLite controlado por `try ... conn.commit()` y `except ... conn.rollback()`.
- **Decisión Técnica:** **ADOPTADO.** Esta recomendación cumple con el estándar de integridad referencial bancaria (propiedades ACID), asegurando que si ocurre un error al persistir cualquiera de los movimientos (depósito, giro o cargo), no queden registros huérfanos de transacciones sin detalle en la base de datos.
