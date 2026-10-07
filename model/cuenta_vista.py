from model.cuenta import Cuenta
from model.enums import TipoCuenta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.cliente import Cliente

class CuentaVista(Cuenta):
    """
    Subtipo de Cuenta Bancaria: Cuenta Vista (Cuenta RUT / Chequera Electrónica).
    Demuestra Herencia (super().__init__), Encapsulamiento y Polimorfismo.
    """
    def __init__(self, numero_cuenta: str, titular: 'Cliente', saldo: float = 0.0):
        super().__init__(numero_cuenta, titular, TipoCuenta.VISTA, saldo)

    def calcularSaldoDisponible(self) -> float:
        """
        Sobrescribe método base: Saldo disponible estricto (sin sobregiro).
        """
        return self._saldo

    def calcularInteres(self) -> float:
        """
        Sobrescribe método abstracto (Polimorfismo):
        Las Cuentas Vista no generan intereses (retorna 0.0).
        """
        return 0.0

    def __str__(self) -> str:
        return f"{super().__str__()} | Tipo: Sin Línea de Crédito / Interés"
