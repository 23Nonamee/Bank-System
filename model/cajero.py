from model.empleado import Empleado
from model.enums import TipoEmpleado
from model.rut import Rut
from model.cuenta import Cuenta

class Cajero(Empleado):
    """
    Subtipo de Empleado: Cajero bancario.
    """
    def __init__(self, nombre: str, rut: Rut, usuario: str, password: str):
        super().__init__(nombre, rut, TipoEmpleado.CAJERO, usuario, password)

    def depositarDinero(self, cuenta: Cuenta, monto: float) -> None:
        """Realiza un depósito en la cuenta señalada."""
        cuenta.ingresarDinero(monto)

    def giroDinero(self, cuenta: Cuenta, monto: float) -> None:
        """Realiza un giro/retiro de dinero de la cuenta señalada."""
        cuenta.retirarDinero(monto)
