from model.cuenta import Cuenta
from model.enums import TipoCuenta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.cliente import Cliente

class CuentaAhorro(Cuenta):
    """
    Subtipo de Cuenta Bancaria: Cuenta de Ahorro.
    Demuestra Herencia (super().__init__), Encapsulamiento y Polimorfismo.
    """
    def __init__(self, numero_cuenta: str, titular: 'Cliente', saldo: float = 0.0, tasa_interes: float = 0.04):
        super().__init__(numero_cuenta, titular, TipoCuenta.AHORRO, saldo)
        self._tasa_interes = 0.0
        self.tasa_interes = tasa_interes  # Invoca setter con validación

    @property
    def tasa_interes(self) -> float:
        return self._tasa_interes

    @tasa_interes.setter
    def tasa_interes(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or valor < 0 or valor > 1:
            raise ValueError("La tasa de interés debe ser un porcentaje expresado entre 0 y 1.0 (ej: 0.04 para 4%).")
        self._tasa_interes = float(valor)

    def calcularInteres(self) -> float:
        """
        Sobrescribe método abstracto (Polimorfismo):
        Genera un interés positivo a favor según la tasa de interés anual aplicada al saldo.
        """
        return self._saldo * self._tasa_interes

    def reajustarInteres(self, valor_uf: float) -> float:
        """
        Reajusta el interés abonado según la variación de la UF (método del diagrama UML).
        """
        if valor_uf <= 0:
            raise ValueError("El valor de la UF debe ser un monto positivo.")
        reajuste = (self._saldo / valor_uf) * self._tasa_interes
        return reajuste

    def __str__(self) -> str:
        interes_estimado = self.calcularInteres()
        return f"{super().__str__()} | Tasa Interés: {self._tasa_interes * 100:.1f}% | Interés Anual: ${interes_estimado:,.0f}"
