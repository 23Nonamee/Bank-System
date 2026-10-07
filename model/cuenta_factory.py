from typing import Optional
from model.enums import TipoCuenta
from model.cliente import Cliente
from model.cuenta import Cuenta
from model.cuenta_corriente import CuentaCorriente
from model.cuenta_ahorro import CuentaAhorro
from model.cuenta_vista import CuentaVista

class CuentaFactory:
    """
    Patrón de Diseño Creacional Factory Method (diagrama UML).
    Abstrae la creación de los distintos tipos de cuentas bancarias.
    """
    @staticmethod
    def crearCuenta(tipo_cuenta: TipoCuenta, cliente: Cliente, numero_cuenta: str, saldo_inicial: float = 0.0, **kwargs) -> Cuenta:
        if not isinstance(tipo_cuenta, TipoCuenta):
            raise TypeError("tipo_cuenta debe ser un valor de TipoCuenta (CORRIENTE, AHORRO, VISTA).")

        if tipo_cuenta == TipoCuenta.CORRIENTE:
            cupo = kwargs.get('cupo_sobregiro', 100000)
            return CuentaCorriente(numero_cuenta=numero_cuenta, titular=cliente, saldo=saldo_inicial, cupo_sobregiro=cupo)
        
        elif tipo_cuenta == TipoCuenta.AHORRO:
            tasa = kwargs.get('tasa_interes', 0.04)
            return CuentaAhorro(numero_cuenta=numero_cuenta, titular=cliente, saldo=saldo_inicial, tasa_interes=tasa)
        
        elif tipo_cuenta == TipoCuenta.VISTA:
            return CuentaVista(numero_cuenta=numero_cuenta, titular=cliente, saldo=saldo_inicial)
        
        else:
            raise ValueError(f"Tipo de cuenta no soportado: {tipo_cuenta}")
