from typing import List, TYPE_CHECKING
from model.rut import Rut
from model.mora import Mora

if TYPE_CHECKING:
    from model.cuenta import Cuenta

class Cliente:
    """
    Clase que representa un Cliente del Banco.
    Relaciones UML:
    - Agregación con Cuenta: Cliente agrupa Cuentas asociadas.
    - Composición/Asociación con Rut y Mora.
    """
    def __init__(self, nombre: str, rut: Rut, mora: Mora = None):
        self._nombre = None
        self.nombre = nombre  # Setter con validación
        self._rut_cliente = rut if isinstance(rut, Rut) else Rut(rut)
        self._mora_cliente = mora if isinstance(mora, Mora) else Mora()
        self._cuentas_asociadas: List['Cuenta'] = []

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValueError("El nombre del cliente debe ser un texto válido con al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def rut_cliente(self) -> Rut:
        return self._rut_cliente

    @property
    def mora_cliente(self) -> Mora:
        return self._mora_cliente

    def tieneMoraVigente(self) -> bool:
        """Indica si el cliente posee una mora activa."""
        return self._mora_cliente.getIsMora()

    def agregarCuenta(self, cuenta: 'Cuenta') -> None:
        """
        Agregación UML: Añade un objeto Cuenta ya existente a la lista de cuentas asociadas.
        """
        if cuenta not in self._cuentas_asociadas:
            self._cuentas_asociadas.append(cuenta)

    def getCuentasAsociadas(self) -> List['Cuenta']:
        """Retorna una copia de las cuentas bancarias asociadas."""
        return list(self._cuentas_asociadas)

    def __str__(self) -> str:
        mora_str = f" [MORA: ${self._mora_cliente.amount_mora:,.0f}]" if self.tieneMoraVigente() else ""
        return f"Cliente: {self._nombre} | RUT: {self._rut_cliente.getFormatedRut()}{mora_str}"

    def __repr__(self) -> str:
        return f"Cliente(nombre='{self._nombre}', rut='{self._rut_cliente.getFormatedRut()}')"
