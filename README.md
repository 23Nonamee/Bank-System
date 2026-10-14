# 🏛️ SouthPark Bank - Core Bancario & Plataforma Digital

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![SQLite3](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-19%2F19%20Pasan-success)
![Frontend](https://img.shields.io/badge/UI-CLI%20%2B%20Web%20GUI-0284c7)
![Seguridad](https://img.shields.io/badge/Seguridad-CWE--89%20%7C%20M%C3%B3dulo%2011-darkgreen)

Plataforma bancaria orientada a objetos desarrollada en **Python** y **JavaScript/HTML/CSS puro**, implementando persistencia transaccional en **SQLite**, arquitectura desacoplada en capas (Modelo, DAO, Servicios, CLI y Web GUI), consumo resiliente de APIs financieras externas y validación defensiva integral.

---

## 📋 Tabla de Contenidos

1. [Información Académica y Negocio](#1-información-académica-y-negocio)
2. [Arquitectura y Estructura del Proyecto](#2-arquitectura-y-estructura-del-proyecto)
3. [Cómo Instalar y Ejecutar Paso a Paso](#3-cómo-instalar-y-ejecutar-paso-a-paso)
   - [3.1. Requisitos y Dependencias](#31-requisitos-y-dependencias)
   - [3.2. Selector Interactivo de Ejecución](#32-selector-interactivo-de-ejecución)
   - [3.3. Modo Interfaz Gráfica (Web GUI)](#33-modo-interfaz-gráfica-web-gui)
   - [3.4. Modo Consola (CLI Interactivo)](#34-modo-consola-cli-interactivo)
4. [Usuarios y Perfiles de Prueba (Multi-Rol)](#4-usuarios-y-perfiles-de-prueba-multi-rol)
5. [Guía de Pruebas Oficial del Guion Docente (P01 a P19)](#5-guía-de-pruebas-oficial-del-guion-docente-p01-a-p19)
6. [Decisiones de Seguridad y Programación Defensiva](#6-decisiones-de-seguridad-y-programación-defensiva)
7. [Bitácora de Uso y Decisiones con Inteligencia Artificial](#7-bitácora-de-uso-y-decisiones-con-inteligencia-artificial)

---

## 1. Información Académica y Negocio

- **Institución:** INACAP - Sede Puente Alto
- **Carrera:** Ingeniería Informática
- **Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)
- **Docente:** Michael Arjel
- **Estudiante:** Isaias Arancibia (RUT: 21.873.976-8)
- **Equipo:** *(Trabajo Individual)*
- **Negocio:** Banco (**SouthPark Bank**)
- **Servicios Externos:** API pública de [mindicador.cl](https://mindicador.cl) (Dólar Observado y Unidad de Fomento).

---

## 2. Arquitectura y Estructura del Proyecto

El sistema aplica una estricta separación de responsabilidades en capas desacopladas:

```text
Bank-System/
├── model/                     # Capa de Dominio (POO pura)
│   ├── cliente.py             # Entidad Cliente con validaciones defensivas
│   ├── rut.py                 # Encapsulamiento y algoritmo Módulo 11 oficial
│   ├── mora.py                # Estado y montos de morosidad
│   ├── cuenta.py              # Clase abstracta base (@abstractmethod, saldo, sobregiro)
│   ├── cuenta_corriente.py    # Subtipo con cupo de sobregiro
│   ├── cuenta_ahorro.py       # Subtipo con tasa de interés y reajuste UF
│   ├── cuenta_vista.py        # Subtipo polimórfico sin sobregiro ni interés
│   ├── cuenta_factory.py      # Patrón Factory Method (bloqueo por mora P15)
│   ├── transaccion.py         # Cabecera de transacción bancaria
│   ├── movimiento.py          # Detalle de movimiento (Composición UML)
│   ├── cartola.py             # Generador de estados de cuenta
│   ├── empleado.py            # Clase base de funcionarios del banco
│   ├── cajero.py              # Subtipo Empleado: operaciones de ventanilla
│   ├── ejecutivo.py           # Subtipo Empleado: apertura de cuentas y clientes
│   └── enums.py               # Enumeraciones de dominio (TipoCuenta, TipoMovimiento, etc.)
│
├── dao/                       # Capa de Acceso a Datos (Persistencia SQLite3)
│   ├── database.py            # Conexión, PRAGMA foreign_keys y creación autónoma de tablas
│   ├── cliente_dao.py         # CRUD parametrizado para Clientes (anti SQL Injection)
│   ├── cuenta_dao.py          # CRUD parametrizado y reconstrucción polimórfica de Cuentas
│   └── transaccion_dao.py     # Transaccionalidad atómica Cabecera-Detalle (ACID)
│
├── services/                  # Servicios de Integración Externa
│   └── indicador_service.py   # Consumo de mindicador.cl con timeout explícito y User-Agent
│
├── frontend/                  # Interfaz Gráfica Web Multi-Rol (HTML5, CSS3 y Vanilla JS)
│   ├── index.html             # Estructura semántica, accesible y vistas SPA
│   ├── styles.css             # Diseño corporativo bancario sobrio y responsive
│   └── app.js                 # Lógica cliente, validaciones Módulo 11 y simulación de roles
│
├── exceptions.py              # Jerarquía de excepciones de dominio y seguridad
├── main.py                    # Entrada principal con selector (CLI o Web GUI) y pruebas P01-P19
├── requirements.txt           # Dependencias oficiales (requests>=2.31.0)
└── banco.db                   # Base de datos SQLite local generada automáticamente
```

---

## 3. Cómo Instalar y Ejecutar Paso a Paso

El software requiere **Python 3.10 o superior**. Al ejecutarse, detecta automáticamente la presencia de la base de datos y crea sus tablas si aún no existen.

### 3.1. Requisitos y Dependencias

1. **Abrir la terminal** y situarse en la raíz del repositorio:
   ```bash
   cd Bank-System
   ```

2. **(Opcional pero recomendado) Crear un entorno virtual:**
   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Instala `requests>=2.31.0` para la consulta de divisas en tiempo real).*

---

### 3.2. Selector Interactivo de Ejecución

Inicia el programa con:
```bash
python main.py
```
*(O `python3 main.py` según la configuración de tu sistema).*

El sistema presentará el **selector principal de modo**:
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

> **Atajos por línea de comandos:**  
> - `python main.py --cli` : Entra directo al menú en consola.  
> - `python main.py --gui` : Levanta el servidor local y abre el navegador web.  
> - `python main.py --test` : Ejecuta directamente la batería docente de pruebas P01 a P19.

---

### 3.3. Modo Interfaz Gráfica (Web GUI)

Al seleccionar la opción **`2`**, el sistema:
1. Inicia un servidor web local en segundo plano en `http://localhost:8000` (o el siguiente puerto libre disponible).
2. **Abre automáticamente tu navegador web predeterminado** con la plataforma web de **SouthPark Bank**.
3. Al presionar <kbd>Enter</kbd> en la terminal, el servidor web se detiene de forma limpia.

*(También puedes abrir directamente [frontend/index.html](file:///home/noname/Desktop/projects/Bank-System/frontend/index.html) haciendo doble clic en el archivo).*

---

### 3.4. Modo Consola (CLI Interactivo)

Al seleccionar la opción **`1`**, se despliega el menú tradicional interactivo por terminal:
- **`1`**: Gestión de Clientes (Crear, Listar, Modificar dirección, Eliminar).
- **`2`**: Gestión de Cuentas (Creación polimórfica con `CuentaFactory`).
- **`3`**: Operaciones Bancarias (Depósitos, Giros y Transferencias).
- **`4`**: Cartola Bancaria (Consulta de transacciones y movimientos).
- **`5`**: Indicadores Económicos (Consulta oficial de UF y Dólar vía API externa).
- **`6`**: **Batería Automatizada de Pruebas Docente (P01 a P19)**.
- **`0`**: Salir de forma limpia asegurando persistencia en disco.

---

## 4. Usuarios y Perfiles de Prueba (Multi-Rol)

Para facilitar la evaluación docente, la pantalla de inicio de sesión de la Web GUI cuenta con **botones de 1 clic** (`[👤 Cliente] [💵 Cajero] [💼 Ejecutivo] [🛡️ Admin]`) que completan automáticamente las credenciales:

| Perfil | Usuario / RUT | Clave | Funcionalidades Destacadas |
| :--- | :--- | :---: | :--- |
| **👤 Cliente Titular**<br>*(Isaias Arancibia)* | `cliente`<br>`12.345.678-5` | `123456` | • Resumen de saldos, sobregiro y disponibilidad combinada.<br>• Cartola bancaria de últimos movimientos.<br>• Transferencias electrónicas con modal de confirmación.<br>• Calculadora de divisas Dólar ↔ Peso en tiempo real. |
| **💵 Cajero Bancario**<br>*(Juan Morales)* | `cajero`<br>`14.253.647-8` | `123456` | • Módulo de ventanilla para **Depósitos** y **Giros** en efectivo.<br>• Validación de saldo insuficiente (**P14**).<br>• Bloqueo automático de giros para clientes en mora (**P15**).<br>• Consulta de estado de cualquier cuenta del banco. |
| **💼 Ejecutivo de Cuentas**<br>*(Andrea Soto)* | `ejecutivo`<br>`15.364.758-9` | `123456` | • **Apertura de Cuentas (`CuentaFactory`):** Corriente, Ahorro y Vista.<br>• **Regla Bloqueante P15:** Alerta defensiva si el cliente registra morosidad.<br>• **Alta de Clientes:** Validación de RUT Módulo 11 y dirección mínima. |
| **🛡️ Administrador**<br>*(Carlos Admin)* | `admin`<br>`11.111.111-1` | `123456` | • Acceso total a todas las vistas del banco.<br>• Métricas consolidadas (fondos custodiados, clientes y cuentas).<br>• **Ejecutor Web de Pruebas Docente:** Visualiza los 19 casos en vivo.<br>• **Simulador de Morosidad:** Activa/desactiva la mora de cualquier cliente para probar los bloqueos. |

---

## 5. Guía de Pruebas Oficial del Guion Docente (P01 a P19)

Para verificar el cumplimiento de los 19 casos de prueba, selecciona la opción **`6`** en la consola o el botón **"▶️ Ejecutar las 19 Pruebas"** en el panel de Administrador:

| N° | Caso de Prueba | Entrada de Prueba | Comportamiento del Sistema | Estado |
| :---: | :--- | :--- | :--- | :---: |
| **P01** | El programa se ejecuta | `python main.py` | Inicia menú interactivo sin errores de inicio | ✅ CUMPLE |
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

## 6. Decisiones de Seguridad y Programación Defensiva

### 6.1. Prevención de Inyección SQL (CWE-89)
La persistencia de datos implementada en `dao/` utiliza exclusivamente la librería estándar oficial `sqlite3` aplicando consultas parametrizadas mediante marcadores de posición posicionales (`?`).
- **Prohibición estricta:** Ninguna sentencia concatena texto ni utiliza formateo de cadenas con datos provistos por el usuario.
- **Transaccionalidad Atómica (ACID):** El registro de transacciones compuestas se ejecuta dentro de bloques `try ... conn.commit()` y `except ... conn.rollback()`.

```python
# SEGURO (dao/cliente_dao.py): Consultas parametrizadas con marcadores (?)
sql = """
    INSERT INTO clientes (rut, nombre, direccion, is_mora, amount_mora)
    VALUES (?, ?, ?, ?, ?);
"""
cursor.execute(sql, (rut_fmt, cliente.nombre, cliente.direccion, is_mora, amount_mora))
conn.commit()
```

### 6.2. Validación Defensiva de Entradas
1. **Algoritmo Módulo 11 Chileno (`model/rut.py`):** El setter `@identificador.setter` valida estrictamente el dígito verificador.
2. **Encapsulamiento en Setters (`model/cliente.py`, `model/cuenta.py`):** Validación de tipos (`str`, `float`, `int`), longitudes mínimas y valores estrictamente positivos.
3. **Manejo Resiliente de APIs Externas (`services/indicador_service.py`):** Captura específica de `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, `requests.exceptions.HTTPError` y `json.JSONDecodeError`, evitando que caídas de internet interrumpan la operación del software.

---

## 7. Bitácora de Uso y Decisiones con Inteligencia Artificial

Durante el desarrollo asistido con Inteligencia Artificial, se analizaron técnicamente diversas propuestas, aplicando criterio profesional para adoptar, modificar o descartar componentes conforme a la rúbrica de evaluación:

### Caso 1: Descarte de Consultas Dinámicas con Formateo de Texto (SQL Injection)
- **Sugerencia de la IA:** Para el método `actualizar` de `ClienteDAO`, la IA propuso concatenar nombres de campos y valores mediante diccionarios y f-strings (`f"UPDATE clientes SET {campo} = '{valor}' WHERE rut = '{rut}'"`), argumentando que permitía actualizar únicamente los campos modificados.
- **Decisión Técnica:** **DESCARTADO.** Concatenar cadenas directamente en sentencias SQL introduce vulnerabilidades críticas de inyección SQL (CWE-89). Se descartó la sugerencia y se implementó una consulta SQL explícita con marcadores parametrizados `?` que pasa todos los valores como parámetros vinculados del motor SQLite.

### Caso 2: Modificación del Manejo de Excepciones en el Consumo de API
- **Sugerencia de la IA:** En el módulo de consumo de la API de indicadores externos (`mindicador.cl`), la IA sugirió envolver toda la petición en un bloque genérico `try ... except Exception as e: return None`.
- **Decisión Técnica:** **MODIFICADO.** Un bloque `except Exception` genérico viola los principios de manejo seguro de errores (Criterio 3.1.3), ya que silencia errores de red, impide distinguir un timeout de una falta de conectividad y enmascara fallos estructurales en los datos. Se modificó el código para capturar de forma específica `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`, `requests.exceptions.HTTPError` y `json.JSONDecodeError`, mapeándolos a excepciones de dominio explícitas (`ApiTimeoutError`, `ApiConexionError`, `ApiIndicadorError`).

### Caso 3: Adopción del Patrón de Persistencia Atómica Transacción-Movimientos
- **Sugerencia de la IA:** Implementar la inserción de la cabecera `transacciones` y sus líneas hijas `movimientos` dentro de un único contexto transaccional SQLite controlado por `try ... conn.commit()` y `except ... conn.rollback()`.
- **Decisión Técnica:** **ADOPTADO.** Esta recomendación cumple con el estándar de integridad referencial bancaria (propiedades ACID), asegurando que si ocurre un error al persistir cualquiera de los movimientos (depósito, giro o cargo), no queden registros huérfanos de transacciones sin detalle en la base de datos.
