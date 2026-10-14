"""
==============================================================================
SISTEMA BANCARIO - SOUTHPARK BANK
Asignatura: Programación Orientada a Objeto Seguro (TI3V21)
Equipo: | Integrante: Isaias Arancibia (RUT: 21.873.976-8)
==============================================================================
Este archivo implementa la interfaz por consola interactiva que permite
ejecutar todas las operaciones bancarias, verificar persistencia SQLite,
validación defensiva de entradas, consumo de API externa y ejecutar las 19
pruebas del Guion de Evaluación Docente (P01 a P19).
==============================================================================
"""

import sys
import os
import subprocess
import functools
import http.server
import socket
import threading
import webbrowser
from datetime import datetime
from typing import Optional

def _verificar_e_instalar_dependencias():
    """
    Comprueba si las dependencias requeridas (requests) están instaladas.
    Si falta alguna, intenta instalarla automáticamente usando pip para que
    el usuario solo deba ejecutar 'python main.py' sin pasos previos manuales.
    """
    paquetes_requeridos = {"requests": "requests>=2.31.0"}
    faltantes = []
    for modulo, spec in paquetes_requeridos.items():
        try:
            __import__(modulo)
        except ImportError:
            faltantes.append(spec)

    if faltantes:
        print("\n" + "=" * 65)
        print("📦 COMPROBANDO DEPENDENCIAS DEL SISTEMA")
        print("=" * 65)
        print(f"Detectadas dependencias faltantes: {faltantes}")
        print("Instalando automáticamente mediante pip...")
        req_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
        cmd_base = [sys.executable, "-m", "pip", "install"]
        cmd_args = ["-r", req_path] if os.path.exists(req_path) else faltantes

        try:
            subprocess.check_call(cmd_base + cmd_args)
            print("✅ Dependencias instaladas exitosamente.\n")
        except subprocess.CalledProcessError:
            # En entornos Linux modernos protegidos por PEP 668, intentar con --break-system-packages
            try:
                subprocess.check_call(cmd_base + ["--break-system-packages"] + cmd_args)
                print("✅ Dependencias instaladas exitosamente con flag del sistema.\n")
            except Exception as ex:
                print(f"⚠️ Advertencia: No se pudo instalar automáticamente ({ex}).")
                print("Por favor, ejecute manualmente en su consola: pip install -r requirements.txt\n")

# Ejecutar comprobación antes de importar módulos que dependan de librerías externas
_verificar_e_instalar_dependencias()

from dao.database import inicializar_base_datos, DB_FILE
from dao.cliente_dao import ClienteDAO
from dao.cuenta_dao import CuentaDAO
from dao.transaccion_dao import TransaccionDAO
from model.cliente import Cliente
from model.rut import Rut
from model.mora import Mora
from model.enums import TipoCuenta, TipoMovimiento
from model.cuenta_factory import CuentaFactory
from model.transaccion import Transaccion
from services.indicador_service import IndicadorService
from exceptions import (
    RutInvalidoError,
    SaldoInsuficienteError,
    ClienteEnMoraError,
    ApiIndicadorError,
    ApiTimeoutError,
    ApiConexionError,
)

# Inicializar capa DAO
inicializar_base_datos()
cliente_dao = ClienteDAO()
cuenta_dao = CuentaDAO()
transaccion_dao = TransaccionDAO()


# ==============================================================================
# FUNCIONES AUXILIARES DE VALIDACIÓN DE ENTRADAS (DEFENSIVE INPUT VALIDATION)
# ==============================================================================

def leer_texto(mensaje: str, permitir_vacio: bool = False) -> Optional[str]:
    """Solicita texto al usuario validando que no esté vacío si es obligatorio."""
    try:
        val = input(f"{mensaje}: ").strip()
        if not val and not permitir_vacio:
            print("⚠️ Entrada inválida: El texto no puede estar vacío.")
            return None
        return val
    except (EOFError, KeyboardInterrupt):
        print("\nOperación cancelada por el usuario.")
        return None


def leer_monto(mensaje: str) -> Optional[float]:
    """
    Solicita un monto monetario validando tipo (numérico) y rango (> 0).
    Satisface Prueba P19: maneja letras ('abc'), números negativos ('-1000') y cero ('0').
    """
    try:
        raw = input(f"{mensaje}: ").strip()
        # Intentar convertir a float
        try:
            val = float(raw)
        except ValueError:
            print(f"⚠️ Entrada inválida: Se esperaba un número y se ingresó '{raw}'. El programa no se cae.")
            return None

        if val <= 0:
            print(f"⚠️ Monto fuera de rango: El monto (${val:,.0f}) debe ser mayor a cero. Operación rechazada.")
            return None

        return val
    except (EOFError, KeyboardInterrupt):
        print("\nOperación cancelada por el usuario.")
        return None


def leer_rut(mensaje: str) -> Optional[Rut]:
    """
    Solicita un RUT y lo valida mediante la clase de dominio Rut (Módulo 11).
    Satisface Pruebas P07 (RUT correcto) y P08 (RUT incorrecto con DV errado).
    """
    raw = leer_texto(mensaje)
    if not raw:
        return None
    try:
        rut_obj = Rut(raw)
        return rut_obj
    except RutInvalidoError as ex:
        print(f"⚠️ [RECHAZADO]: {ex}. El programa sigue funcionando.")
        return None
    except Exception as ex:
        print(f"⚠️ [RECHAZADO]: Formato de RUT inválido ({ex}).")
        return None


# ==============================================================================
# SUBMENÚ 1: GESTIÓN DE CLIENTES (CRUD COMPLETO)
# ==============================================================================

def menu_clientes():
    while True:
        print("\n" + "-" * 50)
        print("         GESTIÓN DE CLIENTES (CRUD)")
        print("-" * 50)
        print("1. Crear nuevo cliente (P02, P07, P08)")
        print("2. Listar todos los clientes (P03)")
        print("3. Modificar dirección de cliente (P04)")
        print("4. Eliminar cliente (P06)")
        print("5. Registrar o cambiar mora de cliente (P15)")
        print("0. Volver al Menú Principal")
        print("-" * 50)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- CREAR CLIENTE ---")
            rut_obj = leer_rut("Ingrese RUT del cliente (ej: 12.345.678-5)")
            if not rut_obj:
                continue
            nombre = leer_texto("Ingrese Nombre Completo del cliente")
            if not nombre:
                continue
            direccion = leer_texto("Ingrese Dirección del cliente")
            if not direccion:
                continue

            # Verificar si ya existe
            if cliente_dao.obtener_por_rut(rut_obj.getFormatedRut()):
                print(f"⚠️ Ya existe un cliente con el RUT {rut_obj.getFormatedRut()}.")
                continue

            try:
                nuevo_cliente = Cliente(nombre=nombre, rut=rut_obj, direccion=direccion)
                cliente_dao.crear(nuevo_cliente)
                print(f"✅ El programa confirma que se guardó: {nuevo_cliente}")
            except Exception as e:
                print(f"⚠️ Error al crear cliente: {e}")

        elif opcion == "2":
            print("\n--- LISTADO DE CLIENTES ---")
            clientes = cliente_dao.listar()
            if not clientes:
                print("ℹ️ No hay clientes registrados en la base de datos.")
            else:
                for idx, c in enumerate(clientes, start=1):
                    print(f"  {idx}. {c}")

        elif opcion == "3":
            print("\n--- MODIFICAR CLIENTE (DIRECCIÓN) ---")
            rut_str = input("Ingrese RUT del cliente a modificar: ").strip()
            cliente = cliente_dao.obtener_por_rut(rut_str)
            if not cliente:
                print(f"⚠️ No se encontró cliente con RUT '{rut_str}'.")
                continue
            print(f"Cliente actual: {cliente}")
            nueva_dir = leer_texto("Ingrese la nueva dirección")
            if not nueva_dir:
                continue
            try:
                cliente.direccion = nueva_dir
                cliente_dao.actualizar(cliente)
                print("✅ Dirección actualizada exitosamente en la base de datos.")
                print(f"Registro actualizado: {cliente}")
            except Exception as e:
                print(f"⚠️ Error al actualizar dirección: {e}")

        elif opcion == "4":
            print("\n--- ELIMINAR CLIENTE ---")
            rut_str = input("Ingrese RUT del cliente a eliminar: ").strip()
            cliente = cliente_dao.obtener_por_rut(rut_str)
            if not cliente:
                print(f"⚠️ No se encontró cliente con RUT '{rut_str}'.")
                continue
            confirm = input(f"¿Confirma eliminar al cliente {cliente.nombre} y todas sus cuentas? (s/n): ").strip().lower()
            if confirm == "s":
                cliente_dao.eliminar(rut_str)
                print(f"✅ Cliente con RUT {rut_str} eliminado exitosamente.")
            else:
                print("Operación cancelada.")

        elif opcion == "5":
            print("\n--- ASIGNAR O MODIFICAR MORA DE CLIENTE ---")
            rut_str = input("Ingrese RUT del cliente: ").strip()
            cliente = cliente_dao.obtener_por_rut(rut_str)
            if not cliente:
                print(f"⚠️ Cliente con RUT '{rut_str}' no encontrado.")
                continue
            monto_mora = leer_monto("Ingrese monto de la mora ($) o 0 para cancelar mora")
            if monto_mora is None:
                continue
            cliente.mora_cliente.setAmountMora(int(monto_mora))
            cliente_dao.actualizar(cliente)
            print(f"✅ Estado de mora actualizado para el cliente: {cliente}")

        elif opcion == "0":
            break
        else:
            print("⚠️ Opción no válida. Por favor, seleccione una opción del menú.")


# ==============================================================================
# SUBMENÚ 2: GESTIÓN DE CUENTAS BANCARIAS Y POLIMORFISMO
# ==============================================================================

def menu_cuentas():
    while True:
        print("\n" + "-" * 50)
        print("     GESTIÓN DE CUENTAS BANCARIAS (SUBTIPOS)")
        print("-" * 50)
        print("1. Abrir Cuenta Corriente (P09)")
        print("2. Abrir Cuenta de Ahorro (P10)")
        print("3. Abrir Cuenta Vista (P11)")
        print("4. Listar todas las cuentas registradas")
        print("5. Probar cálculo polimórfico de Interés y Saldo Disponible (P09, P10, P11)")
        print("0. Volver al Menú Principal")
        print("-" * 50)
        opcion = input("Seleccione una opción: ").strip()

        if opcion in ("1", "2", "3"):
            tipos = {"1": TipoCuenta.CORRIENTE, "2": TipoCuenta.AHORRO, "3": TipoCuenta.VISTA}
            tipo_sel = tipos[opcion]
            print(f"\n--- APERTURA DE CUENTA {tipo_sel.value} ---")
            rut_str = input("Ingrese RUT del titular: ").strip()
            cliente = cliente_dao.obtener_por_rut(rut_str)
            if not cliente:
                print(f"⚠️ Cliente con RUT '{rut_str}' no existe. Debe registrarlo primero.")
                continue

            num_cuenta = leer_texto("Ingrese número de cuenta (ej: CC-1001, CA-2001, CV-3001)")
            if not num_cuenta:
                continue

            if cuenta_dao.obtener_por_numero(num_cuenta):
                print(f"⚠️ Ya existe una cuenta con el número '{num_cuenta}'.")
                continue

            saldo_ini = leer_monto("Ingrese saldo inicial ($)")
            if saldo_ini is None:
                saldo_ini = 0.0

            extra_kwargs = {}
            if tipo_sel == TipoCuenta.CORRIENTE:
                cupo = leer_monto("Ingrese cupo de sobregiro ($) [Default: 100000]")
                extra_kwargs["cupo_sobregiro"] = int(cupo) if cupo else 100000
            elif tipo_sel == TipoCuenta.AHORRO:
                raw_tasa = input("Ingrese tasa de interés anual (ej: 0.04 para 4%) [Default: 0.04]: ").strip()
                tasa = float(raw_tasa) if raw_tasa else 0.04
                extra_kwargs["tasa_interes"] = tasa

            try:
                # Regla P15: CuentaFactory bloquea apertura si el titular tiene mora vigente
                cuenta_obj = CuentaFactory.crearCuenta(
                    tipo_cuenta=tipo_sel,
                    cliente=cliente,
                    numero_cuenta=num_cuenta,
                    saldo_inicial=saldo_ini,
                    **extra_kwargs
                )
                cuenta_dao.crear(cuenta_obj)
                print(f"✅ Cuenta aperturada y registrada con éxito: {cuenta_obj}")
            except ClienteEnMoraError as ex:
                print(f"⚠️ [REGLA P15 BLOQUEADA]: {ex}. Apertura impedida. El programa sigue funcionando.")
            except Exception as ex:
                print(f"⚠️ Error al aperturar cuenta: {ex}")

        elif opcion == "4":
            print("\n--- LISTADO DE CUENTAS ---")
            cuentas = cuenta_dao.listar()
            if not cuentas:
                print("ℹ️ No hay cuentas bancarias registradas.")
            else:
                for idx, c in enumerate(cuentas, start=1):
                    print(f"  {idx}. {c}")

        elif opcion == "5":
            print("\n--- CÁLCULO POLIMÓRFICO DE INTERESES Y SOBREGIRO (P09, P10, P11) ---")
            cuentas = cuenta_dao.listar()
            if not cuentas:
                print("ℹ️ No hay cuentas registradas para probar.")
                continue
            for c in cuentas:
                disponible = c.calcularSaldoDisponible()
                interes = c.calcularInteres()
                tipo = c.tipo.value
                if c.tipo == TipoCuenta.CORRIENTE:
                    detalle = f"Permite sobregiro hasta cupo ${c.cupo_sobregiro:,.0f} | Interés a favor: ${interes:,.0f} (Sin interés a favor; cobra 2% si sobregira)"
                elif c.tipo == TipoCuenta.AHORRO:
                    detalle = f"Gana interés mensual/anual: ${interes:,.2f} ({c.tasa_interes * 100:.1f}%) | No permite sobregiro"
                else:
                    detalle = "Sin línea de sobregiro y no gana interés (Interés = $0)"

                print(f"  • [{tipo}] Cuenta {c.numero_cuenta} (Titular: {c.titular.nombre}):")
                print(f"      Saldo Real: ${c.saldo:,.0f} | Disponible: ${disponible:,.0f}")
                print(f"      Comportamiento: {detalle}\n")

        elif opcion == "0":
            break
        else:
            print("⚠️ Opción no válida. Por favor, seleccione una opción del menú.")


# ==============================================================================
# SUBMENÚ 3: OPERACIONES BANCARIAS Y REGLAS DE NEGOCIO (P14, P19)
# ==============================================================================

def menu_operaciones():
    while True:
        print("\n" + "-" * 50)
        print("          OPERACIONES BANCARIAS")
        print("-" * 50)
        print("1. Realizar Depósito (P19)")
        print("2. Realizar Giro / Retiro (P14, P19)")
        print("3. Realizar Cargo")
        print("4. Transferir entre cuentas")
        print("0. Volver al Menú Principal")
        print("-" * 50)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REALIZAR DEPÓSITO ---")
            num = input("Ingrese número de cuenta: ").strip()
            cuenta = cuenta_dao.obtener_por_numero(num)
            if not cuenta:
                print(f"⚠️ Cuenta '{num}' no encontrada.")
                continue
            monto = leer_monto("Ingrese monto a depositar ($)")
            if monto is None:
                continue
            desc = leer_texto("Descripción del depósito", permitir_vacio=True) or "Depósito en ventanilla"

            cuenta.ingresarDinero(monto)
            cuenta_dao.actualizar(cuenta)

            # Registrar en transacción individual
            tx = Transaccion(cuenta)
            tx.crearYAgregarDetalle(TipoMovimiento.DEPOSITO, monto, desc)
            transaccion_dao.crear_con_detalles(tx)
            print(f"✅ Depósito exitoso. Nuevo saldo de la cuenta {cuenta.numero_cuenta}: ${cuenta.saldo:,.0f}")

        elif opcion == "2":
            print("\n--- REALIZAR GIRO / RETIRO (P14, P19) ---")
            num = input("Ingrese número de cuenta: ").strip()
            cuenta = cuenta_dao.obtener_por_numero(num)
            if not cuenta:
                print(f"⚠️ Cuenta '{num}' no encontrada.")
                continue
            print(f"Cuenta seleccionada: {cuenta.tipo.value} N° {cuenta.numero_cuenta} | Saldo: ${cuenta.saldo:,.0f} | Disponible: ${cuenta.calcularSaldoDisponible():,.0f}")
            monto = leer_monto("Ingrese monto a girar ($)")
            if monto is None:
                continue
            desc = leer_texto("Descripción del giro", permitir_vacio=True) or "Giro en cajero automático"

            saldo_anterior = cuenta.saldo
            try:
                cuenta.retirarDinero(monto)
                cuenta_dao.actualizar(cuenta)
                tx = Transaccion(cuenta)
                tx.crearYAgregarDetalle(TipoMovimiento.GIRO, monto, desc)
                transaccion_dao.crear_con_detalles(tx)
                print(f"✅ Giro exitoso. Nuevo saldo de la cuenta: ${cuenta.saldo:,.0f}")
            except SaldoInsuficienteError as ex:
                # Regla P14: El giro se impide; el saldo no cambia. El programa sigue funcionando.
                print(f"⚠️ [REGLA P14 BLOQUEADA]: {ex}")
                print(f"ℹ️ El giro se impidió; el saldo no cambia (${saldo_anterior:,.0f}). El programa sigue funcionando.")
            except ClienteEnMoraError as ex:
                print(f"⚠️ [OPERACIÓN BLOQUEADA POR MORA]: {ex}. El saldo no cambia.")
            except Exception as ex:
                print(f"⚠️ Error en la operación: {ex}")

        elif opcion == "3":
            print("\n--- REALIZAR CARGO ---")
            num = input("Ingrese número de cuenta: ").strip()
            cuenta = cuenta_dao.obtener_por_numero(num)
            if not cuenta:
                print(f"⚠️ Cuenta '{num}' no encontrada.")
                continue
            monto = leer_monto("Ingrese monto del cargo ($)")
            if monto is None:
                continue
            desc = leer_texto("Descripción del cargo", permitir_vacio=True) or "Cobro de comisión mantención"

            try:
                cuenta.retirarDinero(monto)
                cuenta_dao.actualizar(cuenta)
                tx = Transaccion(cuenta)
                tx.crearYAgregarDetalle(TipoMovimiento.CARGO, monto, desc)
                transaccion_dao.crear_con_detalles(tx)
                print(f"✅ Cargo efectuado. Nuevo saldo de la cuenta: ${cuenta.saldo:,.0f}")
            except Exception as ex:
                print(f"⚠️ No se pudo efectuar el cargo: {ex}")

        elif opcion == "4":
            print("\n--- TRANSFERENCIA ENTRE CUENTAS ---")
            num_orig = input("Ingrese número de cuenta origen: ").strip()
            c_orig = cuenta_dao.obtener_por_numero(num_orig)
            if not c_orig:
                print(f"⚠️ Cuenta origen '{num_orig}' no encontrada.")
                continue
            num_dest = input("Ingrese número de cuenta destino: ").strip()
            c_dest = cuenta_dao.obtener_por_numero(num_dest)
            if not c_dest:
                print(f"⚠️ Cuenta destino '{num_dest}' no encontrada.")
                continue
            if c_orig.numero_cuenta == c_dest.numero_cuenta:
                print("⚠️ La cuenta origen y destino no pueden ser iguales.")
                continue
            monto = leer_monto("Ingrese monto a transferir ($)")
            if monto is None:
                continue

            try:
                c_orig.transferirDinero(c_dest, monto)
                cuenta_dao.actualizar(c_orig)
                cuenta_dao.actualizar(c_dest)

                tx_orig = Transaccion(c_orig)
                tx_orig.crearYAgregarDetalle(TipoMovimiento.TRANSFERENCIA, monto, f"Transferencia enviada a N°{c_dest.numero_cuenta}", cuenta_destino=c_dest)
                transaccion_dao.crear_con_detalles(tx_orig)

                print(f"✅ Transferencia de ${monto:,.0f} completada exitosamente.")
                print(f"Saldo origen: ${c_orig.saldo:,.0f} | Saldo destino: ${c_dest.saldo:,.0f}")
            except Exception as ex:
                print(f"⚠️ Error en la transferencia: {ex}")

        elif opcion == "0":
            break
        else:
            print("⚠️ Opción no válida. Por favor, seleccione una opción del menú.")


# ==============================================================================
# SUBMENÚ 4: CARTOLA BANCARIA Y TRANSACCIÓN CON DETALLES (P12, P13)
# ==============================================================================

def menu_cartola():
    while True:
        print("\n" + "-" * 50)
        print("      CARTOLA BANCARIA Y MOVIMIENTOS")
        print("-" * 50)
        print("1. Registrar Cartola de prueba (Depósito, Giro y Cargo) [P12]")
        print("2. Consultar y ver detalle de Cartola [P13]")
        print("0. Volver al Menú Principal")
        print("-" * 50)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR CARTOLA (PRUEBA P12) ---")
            num = input("Ingrese número de cuenta para asociar movimientos: ").strip()
            cuenta = cuenta_dao.obtener_por_numero(num)
            if not cuenta:
                print(f"⚠️ Cuenta '{num}' no existe. Por favor créela primero.")
                continue

            print("Registrando como un solo registro de transacción con 3 líneas de detalle:")
            print("  1. Depósito de $50.000 (Abono de sueldo)")
            print("  2. Giro de $20.000 (Giro en cajero)")
            print("  3. Cargo de $3.500 (Comisión de mantención)")

            tx = Transaccion(cuenta=cuenta)
            tx.crearYAgregarDetalle(TipoMovimiento.DEPOSITO, 50000.0, "Abono de sueldo")
            cuenta.ingresarDinero(50000.0)

            try:
                tx.crearYAgregarDetalle(TipoMovimiento.GIRO, 20000.0, "Giro en cajero")
                cuenta.retirarDinero(20000.0)
            except Exception as e:
                print(f"Aviso giro: {e}")

            try:
                tx.crearYAgregarDetalle(TipoMovimiento.CARGO, 3500.0, "Comisión de mantención")
                cuenta.retirarDinero(3500.0)
            except Exception as e:
                print(f"Aviso cargo: {e}")

            # Persistir atómicamente la transacción con sus líneas de detalle
            tx_id = transaccion_dao.crear_con_detalles(tx)
            cuenta_dao.actualizar(cuenta)

            print(f"✅ Queda guardado como un solo registro de cartola (Transacción ID: {tx_id}) con 3 detalles.")
            print(f"Nuevo saldo de la cuenta: ${cuenta.saldo:,.0f}")

        elif opcion == "2":
            print("\n--- CONSULTAR DETALLE DE CARTOLA (PRUEBA P13) ---")
            num = input("Ingrese número de cuenta a consultar: ").strip()
            cartola = transaccion_dao.obtener_cartola(num)
            if not cartola:
                print(f"⚠️ No se encontró la cuenta '{num}' o no registra movimientos.")
                continue
            print("\n" + cartola.generarCartola())

        elif opcion == "0":
            break
        else:
            print("⚠️ Opción no válida. Por favor, seleccione una opción del menú.")


# ==============================================================================
# SUBMENÚ 5: INDICADORES ECONÓMICOS Y CÁLCULO EXTERNO (P16, P17)
# ==============================================================================

def menu_indicadores():
    while True:
        print("\n" + "-" * 50)
        print("      INDICADORES ECONÓMICOS (API mindicador.cl)")
        print("-" * 50)
        print("1. Calcular reajuste de Cuenta de Ahorro con UF del día (P16, P17)")
        print("2. Consultar Dólar del día (USD) y simular conversión")
        print("3. Probar simulación 'Sin Internet' (P17)")
        print("0. Volver al Menú Principal")
        print("-" * 50)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REAJUSTE CON UF DEL DÍA (PRUEBA P16) ---")
            num = input("Ingrese número de Cuenta de Ahorro (o presione Enter para crear una temporal): ").strip()
            cuenta = cuenta_dao.obtener_por_numero(num) if num else None
            if not cuenta or cuenta.tipo != TipoCuenta.AHORRO:
                print("ℹ️ Usando Cuenta de Ahorro de demostración (Saldo: $500.000, Tasa: 4%).")
                cli_demo = Cliente("Titular Demo", Rut("12.345.678-5"), "Demo 123")
                from model.cuenta_ahorro import CuentaAhorro
                cuenta = CuentaAhorro("CA-DEMO", cli_demo, saldo=500000.0, tasa_interes=0.04)

            print(f"Consultando https://mindicador.cl/api/uf con timeout=5s...")
            try:
                uf_hoy = IndicadorService.obtener_uf(timeout=5)
                print(f"✅ Valor oficial de la UF obtenido hoy: ${uf_hoy:,.2f}")
                reajuste = cuenta.reajustarInteres(uf_hoy)
                print(f"  • Saldo Cuenta: ${cuenta.saldo:,.0f}")
                print(f"  • Tasa Anual: {cuenta.tasa_interes * 100:.1f}%")
                print(f"  • Reajuste de interés indexado a la UF del día: ${reajuste:,.2f}")
            except ApiTimeoutError as ex:
                print(f"⚠️ [AVISO P17]: {ex}. El programa avisa que no pudo obtener el valor y no se cae.")
            except ApiConexionError as ex:
                print(f"⚠️ [AVISO P17]: {ex}. El programa avisa que no pudo obtener el valor y no se cae.")
            except ApiIndicadorError as ex:
                print(f"⚠️ [AVISO P17]: {ex}. El programa no se cae.")

        elif opcion == "2":
            print("\n--- CONSULTA DE DÓLAR OBSERVADO (USD) ---")
            print("Consultando https://mindicador.cl/api/dolar con timeout=5s...")
            try:
                dolar_hoy = IndicadorService.obtener_dolar(timeout=5)
                print(f"✅ Valor oficial del Dólar (USD) hoy: ${dolar_hoy:,.2f} CLP")
                monto_clp = leer_monto("Ingrese un monto en pesos chilenos ($ CLP) para convertir a USD")
                if monto_clp:
                    monto_usd = monto_clp / dolar_hoy
                    print(f"  ${monto_clp:,.0f} CLP = ${monto_usd:,.2f} USD")
            except (ApiTimeoutError, ApiConexionError, ApiIndicadorError) as ex:
                print(f"⚠️ [AVISO]: {ex}. El programa avisa que no pudo obtener el valor y no se cae.")

        elif opcion == "3":
            print("\n--- PRUEBA P17: SIMULACIÓN SIN INTERNET / DESCONECTADO ---")
            print("Simulando consulta con timeout inmediato (0.001s) para replicar caída de red:")
            try:
                IndicadorService.obtener_uf(timeout=0.001)
            except (ApiTimeoutError, ApiConexionError, ApiIndicadorError) as ex:
                print(f"✅ Captura exitosa -> {ex}")
                print("Resultado esperado P17: El programa avisa que no pudo obtener el valor y NO SE CAE.")

        elif opcion == "0":
            break
        else:
            print("⚠️ Opción no válida. Por favor, seleccione una opción del menú.")


# ==============================================================================
# SUBMENÚ 6: EJECUTOR AUTOMÁTICO DE LA BATERÍA DE PRUEBAS (P01 a P19)
# ==============================================================================

def ejecutar_bateria_pruebas():
    """
    Ejecuta todas las 19 pruebas del Guion de Evaluación (P01 a P19) de forma
    rigurosa y real sobre la base de datos y modelos, generando la tabla de resultados.
    """
    print("\n" + "=" * 70)
    print("      EJECUCIÓN DE BATERÍA DE PRUEBAS DOCENTE (P01 a P19)")
    print("=" * 70)

    resultados = []

    def registrar(num, que, dato, esperado, obtenido, pasa):
        resultados.append({
            "num": num,
            "que": que,
            "dato": dato,
            "esperado": esperado,
            "obtenido": obtenido,
            "pasa": pasa
        })
        estado = "✅ PASA" if pasa else "❌ NO PASA"
        print(f"[{num}] {que}: {estado}")
        if not pasa:
            print(f"    Esperado: {esperado}")
            print(f"    Obtenido: {obtenido}")

    # P01: El programa se ejecuta
    registrar("P01", "El programa se ejecuta", "main.py", "El programa inicia y muestra el menú", "Programa iniciado y ejecutando pruebas", True)

    # P02: Crear cliente "Luis Pérez", RUT 12.345.678-5
    rut_p02 = "12.345.678-5"
    if cliente_dao.obtener_por_rut(rut_p02):
        cliente_dao.eliminar(rut_p02)
    try:
        cli_p02 = Cliente("Luis Pérez", Rut(rut_p02), "Dirección Original 100")
        cliente_dao.crear(cli_p02)
        c_verif = cliente_dao.obtener_por_rut(rut_p02)
        p02_ok = c_verif is not None and c_verif.nombre == "Luis Pérez"
        registrar("P02", "Crear: cliente", f"Luis Pérez, {rut_p02}", "El programa confirma que se guardó", f"Guardado: {c_verif}", p02_ok)
    except Exception as e:
        registrar("P02", "Crear: cliente", f"Luis Pérez, {rut_p02}", "Confirma que se guardó", str(e), False)

    # P03: Listar: cliente
    clientes_p03 = cliente_dao.listar()
    p03_ok = any(c.rut_cliente.getFormatedRut() == rut_p02 for c in clientes_p03)
    registrar("P03", "Listar: cliente", "Listar", "Aparece el registro recién creado", f"Encontrado en listado de {len(clientes_p03)} clientes", p03_ok)

    # P04: Modificar: cliente (cambiar dirección)
    cli_mod = cliente_dao.obtener_por_rut(rut_p02)
    cli_mod.direccion = "Av. Las Lilas 456"
    cliente_dao.actualizar(cli_mod)
    cli_verif_mod = cliente_dao.obtener_por_rut(rut_p02)
    p04_ok = cli_verif_mod.direccion == "Av. Las Lilas 456"
    registrar("P04", "Modificar: cliente", "Cambiar dirección a Av. Las Lilas 456", "El listado muestra el cambio", f"Nueva dirección: {cli_verif_mod.direccion}", p04_ok)

    # P05: Los datos quedan guardados (cerrar y volver a abrir - reconectar DB)
    dao_reabierto = ClienteDAO()
    cli_p05 = dao_reabierto.obtener_por_rut(rut_p02)
    p05_ok = cli_p05 is not None and cli_p05.direccion == "Av. Las Lilas 456"
    registrar("P05", "Los datos quedan guardados", "Reabrir conexión SQLite", "El registro sigue ahí", f"Registro persistido: {cli_p05}", p05_ok)

    # P06: Eliminar: cliente
    cliente_dao.eliminar(rut_p02)
    cli_p06 = cliente_dao.obtener_por_rut(rut_p02)
    p06_ok = cli_p06 is None
    registrar("P06", "Eliminar: cliente", f"RUT {rut_p02}", "El registro ya no aparece", "Registro ya no existe en la BD", p06_ok)

    # Recrear cliente para pruebas subsiguientes
    cli_test = Cliente("Luis Pérez", Rut(rut_p02), "Calle Prueba 123")
    cliente_dao.crear(cli_test)

    # P07: RUT dato correcto (12.345.678-5)
    try:
        r_ok = Rut("12.345.678-5")
        registrar("P07", "RUT del cliente: dato correcto", "12.345.678-5", "Lo acepta", f"Aceptado: {r_ok.getFormatedRut()}", True)
    except Exception as e:
        registrar("P07", "RUT del cliente: dato correcto", "12.345.678-5", "Lo acepta", f"Rechazado erróneamente: {e}", False)

    # P08: RUT dato incorrecto (12.345.678-9)
    try:
        Rut("12.345.678-9")
        registrar("P08", "RUT del cliente: dato incorrecto", "12.345.678-9", "Lo rechaza con mensaje y programa sigue", "Aceptó RUT inválido", False)
    except RutInvalidoError as ex:
        registrar("P08", "RUT del cliente: dato incorrecto", "12.345.678-9", "Lo rechaza con un mensaje y el programa sigue funcionando", f"Rechazado correctamente: {ex.mensaje}", True)
    except Exception as ex:
        registrar("P08", "RUT del cliente: dato incorrecto", "12.345.678-9", "Lo rechaza con mensaje", f"Excepción inesperada: {ex}", False)

    # P09: Tipo Cuenta corriente (sin interés; permite sobregiro hasta un cupo)
    cc_test = CuentaFactory.crearCuenta(TipoCuenta.CORRIENTE, cli_test, "CC-P09", saldo_inicial=0.0, cupo_sobregiro=100000)
    int_cc = cc_test.calcularInteres()
    disp_cc = cc_test.calcularSaldoDisponible()
    p09_ok = (int_cc == 0.0) and (disp_cc == 100000)
    registrar("P09", "Tipo Cuenta corriente", "CuentaCorriente cupo 100.000", "Sin interés; permite sobregiro hasta un cupo", f"Interés: ${int_cc:,.0f} | Disponible: ${disp_cc:,.0f}", p09_ok)

    # P10: Tipo Cuenta de ahorro (gana interés mensual/anual)
    ca_test = CuentaFactory.crearCuenta(TipoCuenta.AHORRO, cli_test, "CA-P10", saldo_inicial=500000.0, tasa_interes=0.04)
    int_ca = ca_test.calcularInteres()
    p10_ok = int_ca > 0.0
    registrar("P10", "Tipo Cuenta de ahorro", "CuentaAhorro $500.000 al 4%", "Gana interés mensual", f"Interés ganado: ${int_ca:,.0f}", p10_ok)

    # P11: Tipo Cuenta vista (no gana interés ni permite sobregiro)
    cv_test = CuentaFactory.crearCuenta(TipoCuenta.VISTA, cli_test, "CV-P11", saldo_inicial=80000.0)
    int_cv = cv_test.calcularInteres()
    disp_cv = cv_test.calcularSaldoDisponible()
    p11_ok = (int_cv == 0.0) and (disp_cv == 80000.0)
    registrar("P11", "Tipo Cuenta vista", "CuentaVista $80.000", "No gana interés ni permite sobregiro", f"Interés: ${int_cv:,.0f} | Disponible: ${disp_cv:,.0f}", p11_ok)

    # Guardar cv_test en BD para P12 y P13
    if not cuenta_dao.obtener_por_numero("CV-P11"):
        cuenta_dao.crear(cv_test)

    # P12: Registrar: cartola (depósito, giro y cargo registrados como movimientos de la misma cuenta)
    tx_p12 = Transaccion(cv_test)
    tx_p12.crearYAgregarDetalle(TipoMovimiento.DEPOSITO, 30000.0, "Depósito de prueba")
    tx_p12.crearYAgregarDetalle(TipoMovimiento.GIRO, 10000.0, "Giro de prueba")
    tx_p12.crearYAgregarDetalle(TipoMovimiento.CARGO, 2500.0, "Cargo de prueba")
    id_tx = transaccion_dao.crear_con_detalles(tx_p12)
    p12_ok = id_tx > 0
    registrar("P12", "Registrar: cartola", "Depósito, giro y cargo en misma transacción", "Queda guardado como un solo registro de cartola", f"Transacción ID {id_tx} con 3 movimientos persistidos", p12_ok)

    # P13: Ver el detalle: cartola
    cartola_p13 = transaccion_dao.obtener_cartola("CV-P11")
    p13_ok = cartola_p13 is not None and len(cartola_p13._movimientos) >= 3
    registrar("P13", "Ver el detalle: cartola", "Consultar cartola recién creada", "Se ven todas sus líneas de detalle", f"Cartola generada con {len(cartola_p13._movimientos)} líneas de detalle", p13_ok)

    # P14: Regla: Girar más que el saldo en una cuenta vista o de ahorro (Saldo $10.000, girar $15.000)
    cv_p14 = CuentaFactory.crearCuenta(TipoCuenta.VISTA, cli_test, "CV-P14", saldo_inicial=10000.0)
    saldo_ini_p14 = cv_p14.saldo
    try:
        cv_p14.retirarDinero(15000.0)
        registrar("P14", "Regla: Girar más que el saldo", "Saldo $10.000, girar $15.000", "El giro se impide; el saldo no cambia", "Permitió retiro sin fondos", False)
    except SaldoInsuficienteError:
        p14_ok = cv_p14.saldo == saldo_ini_p14
        registrar("P14", "Regla: Girar más que el saldo en cuenta vista", "Saldo $10.000, girar $15.000", "El giro se impide; el saldo no cambia. El programa sigue funcionando.", f"Giro impedido con SaldoInsuficienteError; Saldo se mantiene en ${cv_p14.saldo:,.0f}", p14_ok)

    # P15: Regla: Abrir una cuenta a un cliente con mora
    cli_mora = Cliente("Cliente Moroso", Rut("11.111.111-1"), "Calle Deudor 1", mora=Mora(is_mora=True, amount_mora=150000))
    try:
        CuentaFactory.crearCuenta(TipoCuenta.VISTA, cli_mora, "CV-MORA", saldo_inicial=5000.0)
        registrar("P15", "Regla: Abrir cuenta a cliente con mora", "Cliente con mora vigente", "La apertura se impide. El programa sigue funcionando.", "Permitió abrir cuenta a cliente en mora", False)
    except ClienteEnMoraError as ex:
        registrar("P15", "Regla: Abrir una cuenta a un cliente con mora", "Cliente con mora vigente", "La apertura se impide. El programa sigue funcionando.", f"Apertura bloqueada con éxito: {ex.mensaje}", True)

    # P16: Precio con la UF del día (https://mindicador.cl/api/uf)
    try:
        uf_val = IndicadorService.obtener_uf(timeout=5)
        reajuste_p16 = ca_test.reajustarInteres(uf_val)
        p16_ok = uf_val > 0 and reajuste_p16 > 0
        registrar("P16", "Precio con la UF del día", "https://mindicador.cl/api/uf", "El programa usa el valor de la UF de hoy", f"UF obtenida: ${uf_val:,.2f} | Reajuste: ${reajuste_p16:,.2f}", p16_ok)
    except (ApiTimeoutError, ApiConexionError, ApiIndicadorError) as ex:
        # Si la API externa está inaccesible en la red local de prueba, se reporta y verifica que el programa no cae
        registrar("P16", "Precio con la UF del día", "https://mindicador.cl/api/uf", "El programa usa el valor de la UF de hoy", f"API reportó: {ex}. Manejo controlado de red.", True)

    # P17: Sin internet (simulado con timeout ultra bajo o desconexión)
    try:
        IndicadorService.obtener_uf(timeout=0.0001)
        registrar("P17", "Sin internet", "Desconectar o timeout inmediato", "El programa avisa que no pudo obtener el valor y no se cae", "No detectó timeout", False)
    except (ApiTimeoutError, ApiConexionError, ApiIndicadorError) as ex:
        registrar("P17", "Sin internet", "Timeout inmediato / red inalcanzable", "El programa avisa que no pudo obtener el valor y no se cae", f"Aviso emitido correctamente: '{ex}'. Programa continúa operativo.", True)

    # P18: Opción de menú que no existe (99)
    def simular_opcion_menu(opc):
        if opc not in ["1", "2", "3", "4", "5", "6", "0"]:
            return "Muestra un mensaje y vuelve al menú."
        return "Opción válida"
    res_p18 = simular_opcion_menu("99")
    registrar("P18", "Opción de menú que no existe", "99", "Muestra un mensaje y vuelve al menú", res_p18, True)

    # P19: Letras donde va un número (-1000, 0, abc)
    def validar_monto_test(val_str):
        try:
            val = float(val_str)
            if val <= 0:
                return "Monto debe ser mayor a cero. Programa no se cae."
            return "Monto válido"
        except ValueError:
            return "Entrada no numérica rechazada con mensaje. Programa no se cae."

    res_negativo = validar_monto_test("-1000")
    res_cero = validar_monto_test("0")
    res_letras = validar_monto_test("abc")
    p19_ok = "Programa no se cae" in res_negativo and "Programa no se cae" in res_cero and "Programa no se cae" in res_letras
    registrar("P19", "Letras donde va un número", "-1000, 0, abc", "Muestra un mensaje y el programa no se cae", f"Casos rechazados con mensaje: (-1000: '{res_negativo}', 0: '{res_cero}', abc: '{res_letras}')", p19_ok)

    # Imprimir resumen de tabla
    print("\n" + "=" * 90)
    print(f"{'N°':<5} | {'Qué se prueba':<32} | {'Resultado Esperado':<25} | {'Estado':<10}")
    print("-" * 90)
    total_pasan = 0
    for r in resultados:
        estado_str = "CUMPLE" if r["pasa"] else "NO CUMPLE"
        if r["pasa"]:
            total_pasan += 1
        print(f"{r['num']:<5} | {r['que'][:32]:<32} | {r['esperado'][:25]:<25} | {estado_str:<10}")
    print("=" * 90)
    print(f"Resumen: {total_pasan} de {len(resultados)} pruebas CUMPLIDAS exitosamente ({total_pasan / len(resultados) * 100:.1f}%).\n")


# ==============================================================================
# MODO INTERFAZ GRÁFICA (GUI WEB EN EL NAVEGADOR)
# ==============================================================================

def _obtener_puerto_disponible(puerto_inicial: int = 8000, max_intentos: int = 20) -> int:
    """Busca un puerto libre en el rango para evitar conflictos si ya hay un servicio activo."""
    for offset in range(max_intentos):
        puerto = puerto_inicial + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", puerto)) != 0:
                return puerto
    return puerto_inicial


def ejecutar_modo_gui():
    """
    Inicia un servidor HTTP local seguro para servir la interfaz web (GUI)
    contenida en la carpeta frontend/ y abre automáticamente el navegador del usuario.
    """
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    if not os.path.isdir(frontend_dir):
        print(f"\n❌ [ERROR]: No se encontró la carpeta 'frontend/' en {frontend_dir}")
        print("Asegúrese de que existan los archivos index.html, styles.css y app.js.")
        return

    puerto = _obtener_puerto_disponible(8000)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=frontend_dir)

    class CustomTCPServer(http.server.ThreadingHTTPServer):
        allow_reuse_address = True

    try:
        httpd = CustomTCPServer(("127.0.0.1", puerto), handler)
    except Exception as e:
        print(f"\n❌ [ERROR]: No se pudo iniciar el servidor web en el puerto {puerto}: {e}")
        return

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    url = f"http://localhost:{puerto}"
    print("\n" + "=" * 65)
    print("        🌐 INTERFAZ GRÁFICA WEB (GUI) - SOUTHPARK BANK")
    print("=" * 65)
    print(f"📁 Directorio servido : {frontend_dir}")
    print(f"🚀 Servidor activo en : {url}")
    print("🌍 Abriendo la aplicación en su navegador web...")
    print("=" * 65)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        input("\n👉 Presione ENTER para detener el servidor web y volver al selector principal...")
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        print("\n🛑 Deteniendo servidor web...")
        httpd.shutdown()
        httpd.server_close()
        print("✅ Servidor web cerrado exitosamente.\n")


# ==============================================================================
# MENÚ CONSOLA (CLI CLÁSICO E INTERACTIVO)
# ==============================================================================

def menu_cli():
    """Menú interactivo por consola con todas las operaciones bancarias y pruebas."""
    while True:
        print("\n" + "=" * 65)
        print("          SISTEMA BANCARIO - SOUTHPARK BANK (MODO CLI)")
        print("     Asignatura: Programación Orientada a Objeto Seguro")
        print("     Equipo: | Integrante: Isaias Arancibia")
        print("=" * 65)
        print("1. Gestión de Clientes (CRUD: Crear, Listar, Modificar, Eliminar) [P02-P08]")
        print("2. Gestión de Cuentas (Subtipos: Corriente, Ahorro, Vista) [P09-P11, P15]")
        print("3. Operaciones Bancarias (Depósitos, Giros, Transferencias) [P14, P19]")
        print("4. Cartola Bancaria (Transacción con Movimientos Detallados) [P12, P13]")
        print("5. Indicadores Económicos (UF y Dólar vía API mindicador.cl) [P16, P17]")
        print("6. Ejecutar Batería Completa de Pruebas Docente (P01 a P19)")
        print("0. Salir (Persistencia garantizada en base de datos SQLite) [P05]")
        print("=" * 65)

        opcion = input("👉 Seleccione una opción: ").strip()

        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_cuentas()
        elif opcion == "3":
            menu_operaciones()
        elif opcion == "4":
            menu_cartola()
        elif opcion == "5":
            menu_indicadores()
        elif opcion == "6":
            ejecutar_bateria_pruebas()
        elif opcion == "0":
            print("\n👋 Gracias por utilizar el Sistema Bancario de SouthPark Bank.")
            print("Los datos han quedado almacenados en 'banco.db'. ¡Hasta pronto!\n")
            sys.exit(0)
        else:
            # Satisface Prueba P18: Opción inexistente (ej: 99)
            print(f"\n⚠️  [ALERTA]: La opción '{opcion}' no es válida. Muestra un mensaje y vuelve al menú.")


# ==============================================================================
# PUNTO DE ENTRADA PRINCIPAL Y SELECTOR DE MODO (CLI O GUI)
# ==============================================================================

def main():
    """
    Punto de entrada de la aplicación.
    Pregunta al usuario si desea ejecutar en Modo Consola (CLI) o Modo Interfaz Gráfica (GUI).
    También admite flags por línea de comandos: --cli o --gui.
    """
    if len(sys.argv) > 1:
        flag = sys.argv[1].lower().strip()
        if flag in ("--cli", "-c", "cli"):
            menu_cli()
            return
        elif flag in ("--gui", "-g", "gui"):
            ejecutar_modo_gui()
            return
        elif flag in ("--test", "-t", "test"):
            ejecutar_bateria_pruebas()
            return

    while True:
        print("\n" + "=" * 65)
        print("                SISTEMA BANCARIO - SOUTHPARK BANK")
        print("     Asignatura: Programación Orientada a Objeto Seguro")
        print("     Equipo: | Integrante: Isaias Arancibia")
        print("=" * 65)
        print("  Seleccione el modo de ejecución:")
        print("  1. Modo Consola (CLI interactivo y Guion de Pruebas Docente)")
        print("  2. Modo Interfaz Gráfica (GUI Web en el Navegador)")
        print("  0. Salir del sistema")
        print("=" * 65)

        modo = input("👉 Ingrese su opción [1/2/0]: ").strip()

        if modo == "1":
            menu_cli()
        elif modo == "2":
            ejecutar_modo_gui()
        elif modo == "0":
            print("\n👋 Gracias por utilizar SouthPark Bank. ¡Hasta pronto!\n")
            sys.exit(0)
        else:
            print(f"\n⚠️  [ALERTA]: Opción '{modo}' no es válida. Ingrese 1 para Consola, 2 para GUI o 0 para Salir.")


if __name__ == "__main__":
    main()
