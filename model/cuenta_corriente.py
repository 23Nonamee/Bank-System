from model.cuenta import Cuenta
from model.enums import TipoCuenta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.cliente import Cliente

class CuentaCorriente(Cuenta):
    """
    Subtipo de Cuenta Bancaria: Cuenta Corriente.
    Demuestra Herencia (super().__init__), Encapsulamiento y Polimorfismo.
    """
    def __init__(self, numero_cuenta: str, titular: 'Cliente', saldo: float = 0.0, cupo_sobregiro: int = 100000):
        super().__init__(numero_cuenta, titular, TipoCuenta.CORRIENTE, saldo)
        self._cupo_sobregiro = 0
        self.cupo_sobregiro = cupo_sobregiro  # Invoca setter con validación

    @property
    def cupo_sobregiro(self) -> int:
        return self._cupo_sobregiro

    @cupo_sobregiro.setter
    def cupo_sobregiro(self, valor: int) -> None:
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El cupo de sobregiro debe ser un número entero o decimal mayor o igual a 0.")
        self._cupo_sobregiro = int(valor)

    def calcularSaldoDisponible(self) -> float:
        """
        Sobrescribe método base: Saldo disponible = Saldo real + Cupo de sobregiro.
        """
        return self._saldo + self._cupo_sobregiro

    def calcularInteres(self) -> float:
        """
        Sobrescribe método abstracto (Polimorfismo):
        Si la cuenta está girada sobre su saldo real, cobra un 2% mensual por sobregiro.
        De lo contrario, no genera intereses a favor.
        """
        if self._saldo < 0:
            return abs(self._saldo) * 0.02
        return 0.0

    def __str__(self) -> str:
        disp = self.calcularSaldoDisponible()
        return f"{super().__str__()} | Cupo Sobregiro: ${self._cupo_sobregiro:,.0f} | Disponible: ${disp:,.0f}"
