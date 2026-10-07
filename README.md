# Sistema Bancario - Evaluación Sumativa N°2
**Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)  
**Institución:** INACAP - Sede Puente Alto  

## 📌 Descripción del Proyecto
Este repositorio contiene la implementación orientada a objetos en Python del modelo de clases UML diseñado para el **Sistema Bancario**. Cumple rigurosamente con los criterios de evaluación exigidos en la Sumativa N°2.

---

## 🗂️ Estructura del Repositorio
```text
Bank-System/
│
├── model/                         # Clases del modelo (Una clase por archivo)
│   ├── __init__.py
│   ├── rut.py                     # Encapsulamiento y validación Módulo 11 de RUT
│   ├── mora.py                    # Estado y monto de morosidad de clientes
│   ├── cliente.py                 # Agregación con Cuenta, Composición con Rut/Mora
│   ├── enums.py                   # TipoCuenta, TipoMovimiento, TipoEmpleado
│   ├── cuenta.py                  # Clase Abstracta Base (super(), @property, exceptions)
│   ├── cuenta_corriente.py        # Subtipo con cupoSobreGiro y polimorfismo
│   ├── cuenta_ahorro.py           # Subtipo con tasaInteres y polimorfismo
│   ├── cuenta_vista.py            # Subtipo sin línea ni interés (polimorfismo)
│   ├── movimiento.py              # Detalle de transacción
│   ├── transaccion.py             # Composición con Movimientos
│   ├── cuenta_factory.py          # Patrón Factory Method para creación de cuentas
│   ├── empleado.py                # Clase base de empleados con auth hash
│   ├── ejecutivo.py               # Operaciones de ejecutivo bancario
│   ├── cajero.py                  # Operaciones de cajero bancario
│   └── cartola.py                 # Generación de cartolas bancarias
│
├── exceptions.py                  # Excepciones personalizadas del dominio (Reglas de negocio)
├── main.py                        # Script principal de demostración
└── diagrama_banco.drawio          # Diagrama de clases UML original/actualizado
```

---

## 🚀 Ejecución del Script de Demostración
Para verificar la solución de principio a fin:
```bash
python3 main.py
```

---

## 📐 Demostración de Principios POO Implementados
1. **Herencia y `super().__init__()`**: Las clases `CuentaCorriente`, `CuentaAhorro` y `CuentaVista` heredan de la clase base abstracta `Cuenta` invocando explícitamente a `super().__init__()`.
2. **Encapsulamiento**: Atributos privados (`_saldo`, `_identificador`, `_cupo_sobregiro`, etc.) con propiedades `@property` y validaciones defensivas en sus setters.
3. **Polimorfismo**: Las 3 clases hijas sobrescriben los métodos `calcularInteres()` y `calcularSaldoDisponible()`. `main.py` invoca los métodos polimórficos directamente sobre las cuentas sin usar sentencias `if isinstance(...)`.
4. **Relaciones UML**:
   - **Agregación**: `Cliente` agrega objetos `Cuenta` previamente instanciados.
   - **Composición**: `Transaccion` crea y gestiona el ciclo de vida de sus objetos `Movimiento` internos.
5. **Excepciones Propias y Reglas de Negocio**:
   - `RutInvalidoError`: Lanzada al ingresar un RUT con dígito verificador inválido.
   - `SaldoInsuficienteError`: Lanzada al intentar girar o transferir más allá del saldo disponible.
   - `ClienteEnMoraError`: Lanzada al intentar efectuar operaciones con un cliente que registra mora vigente.
