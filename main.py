"""
==============================================================================
SISTEMA BANCARIO - DEMOSTRACIÓN COMPLETA MODELO DE CLASES (POO EN PYTHON)
Asignatura: Programación Orientada a Objeto Seguro (TI3V21)
Evaluación Sumativa N°2
==============================================================================
Este script demuestra todos los requerimientos exigidos por la Rúbrica:
 1. Tres subtipos de cuenta llamando a su método polimórfico (calcularInteres / calcularSaldoDisponible).
 2. Atributos encapsulados con @property y validación defensiva en setter (Validación de RUT y montos).
 3. Transacción con sus líneas de detalle (Relación de Composición Transaccion-Movimiento).
 4. Provocación y captura segura de 2 reglas del negocio mediante try/except.
"""

from model.rut import Rut
from model.mora import Mora
from model.cliente import Cliente
from model.enums import TipoCuenta, TipoMovimiento
from model.cuenta_factory import CuentaFactory
from model.transaccion import Transaccion
from model.cartola import Cartola
from exceptions import RutInvalidoError, SaldoInsuficienteError, ClienteEnMoraError


def banner(titulo: str):
    print("\n" + "=" * 75)
    print(f" {titulo.upper()}")
    print("=" * 75)


def main():
    banner("1. DEMOSTRACIÓN DE ENCAPSULAMIENTO Y VALIDACIÓN EN SETTERS")
    
    # 1.1 Crear RUT válido
    rut_valido = Rut("12.345.678-5")
    print(f"[OK] RUT Creado exitosamente: {rut_valido.getFormatedRut()} (Limpio: '{rut_valido.getRut()}')")

    # 1.2 Probar Setter / Validación de RUT Inválido (Regla de validación)
    print("\n--> Intentando asignar un RUT con dígito verificador erróneo ('12.345.678-9')...")
    try:
        rut_invalido = Rut("12.345.678-9")
    except RutInvalidoError as ex:
        print(f"    [EXCEPCIÓN CAPTURADA EXITOSAMENTE] -> {ex}")

    # 1.3 Crear Cliente
    cliente1 = Cliente(nombre="Carlos Mendoza", rut=rut_valido)
    print(f"[OK] Cliente Creado: {cliente1}")

    banner("2. DEMOSTRACIÓN DE HERENCIA, SUPER() Y SUBTIPOS DE CUENTA (CUENTAFACTORY)")
    
    # Creación de los 3 subtipos de cuenta usando CuentaFactory (Patrón Factory)
    cuenta_corriente = CuentaFactory.crearCuenta(
        tipo_cuenta=TipoCuenta.CORRIENTE,
        cliente=cliente1,
        numero_cuenta="CC-1001",
        saldo_inicial=150000,
        cupo_sobregiro=100000
    )

    cuenta_ahorro = CuentaFactory.crearCuenta(
        tipo_cuenta=TipoCuenta.AHORRO,
        cliente=cliente1,
        numero_cuenta="CA-2001",
        saldo_inicial=500000,
        tasa_interes=0.05
    )

    cuenta_vista = CuentaFactory.crearCuenta(
        tipo_cuenta=TipoCuenta.VISTA,
        cliente=cliente1,
        numero_cuenta="CV-3001",
        saldo_inicial=80000
    )

    cuentas_registradas = [cuenta_corriente, cuenta_ahorro, cuenta_vista]
    for c in cuentas_registradas:
        print(f"[+] {c}")

    banner("3. DEMOSTRACIÓN DE POLIMORFISMO (SIN SENTENCIAS IF SEGÚN TIPO)")
    print("Iterando colección de cuentas llamando al método polimórfico 'calcularInteres()' y 'calcularSaldoDisponible()':\n")
    
    for c in cliente1.getCuentasAsociadas():
        interes = c.calcularInteres()
        disponible = c.calcularSaldoDisponible()
        print(f"Account [{c.numero_cuenta}] ({c.tipo.value}):")
        print(f"   -> Saldo Real: ${c.saldo:,.0f}")
        print(f"   -> Saldo Disponible: ${disponible:,.0f}")
        print(f"   -> Interés Generado/Cobrado (Polimórfico): ${interes:,.2f}\n")

    banner("4. DEMOSTRACIÓN DE RELACIÓN DE COMPOSICIÓN (TRANSACCIÓN CON DETALLES)")
    
    transaccion1 = Transaccion(cuenta=cuenta_corriente)
    
    # Agregar líneas de movimiento (Composición)
    transaccion1.crearYAgregarDetalle(
        tipo=TipoMovimiento.DEPOSITO,
        monto=50000,
        descripcion="Depósito por transferencia de sueldo"
    )
    cuenta_corriente.ingresarDinero(50000)

    transaccion1.crearYAgregarDetalle(
        tipo=TipoMovimiento.GIRO,
        monto=30000,
        descripcion="Giro de efectivo en cajero automático"
    )
    cuenta_corriente.retirarDinero(30000)

    print(transaccion1)
    print(f"\n[OK] Saldo actualizado tras movimientos: ${cuenta_corriente.saldo:,.0f}")

    # Generar Cartola de Movimientos
    cartola = Cartola(
        cuenta=cuenta_corriente,
        fecha_inicio=transaccion1.fecha,
        fecha_fin=transaccion1.fecha,
        movimientos=transaccion1.detalles
    )
    print("\n" + cartola.generarCartola())

    banner("5. DEMOSTRACIÓN DE PROVOCACIÓN Y CAPTURA DE LAS 2 REGLAS DE NEGOCIO")

    # -------------------------------------------------------------------------
    # REGLA DE NEGOCIO 1: Intento de retiro que supera el saldo disponible
    # -------------------------------------------------------------------------
    print("--> REGLA DE NEGOCIO 1: Intentando retirar $500.000 de Cuenta Corriente (Disponible: $240.000)...")
    try:
        cuenta_corriente.retirarDinero(500000)
    except SaldoInsuficienteError as ex:
        print(f"    [REGLA 1 VIOLADA Y CAPTURADA CONTROLADAMENTE] -> {ex}")
    except Exception as ex:
        print(f"    [ERROR INESPERADO] -> {ex}")

    # -------------------------------------------------------------------------
    # REGLA DE NEGOCIO 2: Cliente con Mora Vigente intenta realizar una operación
    # -------------------------------------------------------------------------
    print("\n--> REGLA DE NEGOCIO 2: Asignando Mora de $120.000 al Cliente e intentando retirar dinero...")
    # Asignamos mora al cliente
    cliente1.mora_cliente.setAmountMora(120000)
    print(f"    Estado Cliente actual: {cliente1}")

    try:
        # Intentar realizar un giro teniendo mora vigente
        cuenta_vista.retirarDinero(10000)
    except ClienteEnMoraError as ex:
        print(f"    [REGLA 2 VIOLADA Y CAPTURADA CONTROLADAMENTE] -> {ex}")
    except Exception as ex:
        print(f"    [ERROR INESPERADO] -> {ex}")

    banner("FIN DE DEMOSTRACIÓN - EL PROGRAMA FINALIZÓ SIN ERRORES NO CONTROLADOS")


if __name__ == "__main__":
    main()
