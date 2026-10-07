"""
==============================================================================
SISTEMA BANCARIO INTERACTIVO
Permite ingresar datos a mano por teclado o presionar [Enter] para usar valores por defecto.
==============================================================================
"""

import sys
from model.rut import Rut
from model.cliente import Cliente
from model.enums import TipoCuenta, TipoMovimiento
from model.cuenta_factory import CuentaFactory
from model.transaccion import Transaccion
from model.cartola import Cartola
from exceptions import RutInvalidoError, SaldoInsuficienteError, ClienteEnMoraError


def pedir_dato(mensaje: str, default: str) -> str:
    """Solicita un dato al usuario. Si presiona Enter, retorna el valor por defecto."""
    try:
        val = input(f"👉 {mensaje} [Default: '{default}']: ").strip()
        return val if val else default
    except (EOFError, KeyboardInterrupt):
        return default
    except Exception:
        return default


def main():
    print("\n" + "=" * 65)
    print("      SISTEMA BANCARIO - TERMINAL DE ATENCIÓN INTERACTIVA")
    print("=" * 65 + "\n")

    # 1. Registro y Validación de Cliente
    print("--- PASO 1: REGISTRO Y VALIDACIÓN DE CLIENTE ---")
    
    print("\n[Prueba de validación de RUT erróneo]")
    rut_invalido_input = pedir_dato("Ingrese un RUT inválido para probar el filtro", "12.345.678-9")
    try:
        Rut(rut_invalido_input)
        print("  RUT aceptado.")
    except RutInvalidoError as ex:
        print(f"  ⚠️  [ALERTA DE SEGURIDAD]: {ex}\n")

    print("[Ingreso de cliente con RUT válido]")
    rut_valido_input = pedir_dato("Ingrese RUT válido del cliente", "12.345.678-5")
    nombre_input = pedir_dato("Ingrese Nombre Completo del cliente", "Carlos Mendoza")

    rut_obj = Rut(rut_valido_input)
    cliente = Cliente(nombre=nombre_input, rut=rut_obj)
    print(f"\n✅ Cliente registrado exitosamente: {cliente}\n")

    # 2. Apertura de Cuentas (Herencia, super() y Factory)
    print("--- PASO 2: APERTURA DE CUENTAS BANCARIAS ---")
    
    saldo_cc = float(pedir_dato("Monto inicial Cuenta Corriente CC-1001 ($)", "150000"))
    cupo_cc = int(pedir_dato("Cupo sobregiro Cuenta Corriente ($)", "100000"))
    cc = CuentaFactory.crearCuenta(TipoCuenta.CORRIENTE, cliente, "CC-1001", saldo_inicial=saldo_cc, cupo_sobregiro=cupo_cc)

    saldo_ca = float(pedir_dato("Monto inicial Cuenta Ahorro CA-2001 ($)", "500000"))
    tasa_ca = float(pedir_dato("Tasa interés Cuenta Ahorro (ej: 0.05)", "0.05"))
    ca = CuentaFactory.crearCuenta(TipoCuenta.AHORRO, cliente, "CA-2001", saldo_inicial=saldo_ca, tasa_interes=tasa_ca)

    saldo_cv = float(pedir_dato("Monto inicial Cuenta Vista CV-3001 ($)", "80000"))
    cv = CuentaFactory.crearCuenta(TipoCuenta.VISTA, cliente, "CV-3001", saldo_inicial=saldo_cv)

    print("\n✅ Resumen de cuentas aperturadas:")
    for c in cliente.getCuentasAsociadas():
        print(f"  • {c}")
    print()

    # 3. Transacciones y Movimientos (Composición)
    print("--- PASO 3: OPERACIONES Y TRANSACCIONES EN CC-1001 ---")
    tx = Transaccion(cuenta=cc)

    monto_dep = float(pedir_dato("Monto a depositar ($)", "50000"))
    desc_dep = pedir_dato("Descripción del depósito", "Abono de Remuneración")
    tx.crearYAgregarDetalle(TipoMovimiento.DEPOSITO, monto_dep, desc_dep)
    cc.ingresarDinero(monto_dep)
    print(f"  [+] Depósito registrado. Nuevo saldo: ${cc.saldo:,.0f}\n")

    monto_giro = float(pedir_dato("Monto a girar/retirar ($)", "30000"))
    desc_giro = pedir_dato("Descripción del giro", "Giro Cajero Automático")
    tx.crearYAgregarDetalle(TipoMovimiento.GIRO, monto_giro, desc_giro)
    cc.retirarDinero(monto_giro)
    print(f"  [+] Giro registrado. Nuevo saldo: ${cc.saldo:,.0f}\n")

    print("[Generando Cartola de Movimientos]")
    cartola = Cartola(cuenta=cc, fecha_inicio=tx.fecha, fecha_fin=tx.fecha, movimientos=tx.detalles)
    print(cartola.generarCartola() + "\n")

    # 4. Cálculo Polimórfico
    print("--- PASO 4: CÁLCULO POLIMÓRFICO DE SALDOS E INTERESES ---")
    for c in cliente.getCuentasAsociadas():
        disp = c.calcularSaldoDisponible()
        inte = c.calcularInteres()
        print(f"  • {c.tipo.value} N° {c.numero_cuenta}: Saldo Real = ${c.saldo:,.0f} | Disponible = ${disp:,.0f} | Interés = ${inte:,.2f}")
    print()

    # 5. Reglas de Negocio y Excepciones
    print("--- PASO 5: EVALUACIÓN DE REGLAS DE NEGOCIO Y EXCEIPCIONES ---")
    
    print("\n[Probando Regla 1: Saldo Insuficiente]")
    monto_exceso = float(pedir_dato("Monto a girar que supere el disponible en CC-1001 ($)", "500000"))
    try:
        cc.retirarDinero(monto_exceso)
    except SaldoInsuficienteError as ex:
        print(f"  ❌ Excepción Capturada -> {ex}\n")

    print("[Probando Regla 2: Cliente en Mora]")
    monto_mora = int(pedir_dato("Monto de mora a asignar al cliente ($)", "120000"))
    cliente.mora_cliente.setAmountMora(monto_mora)
    print(f"  Estado cliente: {cliente}")

    print("-> Intentando girar $10.000 de Cuenta Vista con mora activa...")
    try:
        cv.retirarDinero(10000)
    except ClienteEnMoraError as ex:
        print(f"  ❌ Excepción Capturada -> {ex}\n")

    print("=" * 65)
    print("        OPERACIÓN FINALIZADA EXITOSAMENTE Y SIN ERRORES")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
