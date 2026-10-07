from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from model.enums import TipoCuenta
from exceptions import SaldoInsuficienteError, ClienteEnMoraError

if TYPE_CHECKING:
    from model.cliente import Cliente

class Cuenta(ABC):
    """
    Clase Abstracta Base que representa una Cuenta Bancaria.
    Requisitos POO Rúbrica:
    - Encapsulamiento con @property y setter.
    - Método abstracto para polimorfismo (calcularInteres).
    - Excepciones del negocio (SaldoInsuficienteError, ClienteEnMoraError).
    """
    def __init__(self, numero_cuenta: str, titular: 'Cliente', tipo: TipoCuenta, saldo: float = 0.0):
        self._numero_cuenta = str(numero_cuenta).strip()
        self._titular = titular
        self._tipo = tipo
        self._saldo = 0.0
        self.saldo = saldo  # Invoca el setter encapsulado
        
        # Agregación UML: asociar la cuenta al cliente
        if titular and hasattr(titular, 'agregarCuenta'):
            titular.agregarCuenta(self)

    @property
    def numero_cuenta(self) -> str:
        return self._numero_cuenta

    @property
    def titular(self) -> 'Cliente':
        return self._titular

    @property
    def tipo(self) -> TipoCuenta:
        return self._tipo

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        if not isinstance(valor, (int, float)):
            raise TypeError("El saldo debe ser un número válido.")
        self._saldo = float(valor)

    def calcularSaldoDisponible(self) -> float:
        """Retorna el saldo disponible para retiro/transferencia."""
        return self._saldo

    def ingresarDinero(self, cantidad_agregar: float) -> None:
        """Ingresa un monto positivo a la cuenta."""
        if cantidad_agregar <= 0:
            raise ValueError("El monto a ingresar debe ser mayor que cero.")
        self._saldo += float(cantidad_agregar)

    def retirarDinero(self, cantidad_retirar: float) -> None:
        """
        Retira dinero de la cuenta si no supera el saldo disponible.
        Lanza SaldoInsuficienteError si no hay fondos suficientes.
        Regla de negocio: no permite retirar con mora vigente.
        """
        if self._titular and self._titular.tieneMoraVigente():
            raise ClienteEnMoraError(self._titular.nombre, self._titular.mora_cliente.amount_mora)
        
        disponible = self.calcularSaldoDisponible()
        if cantidad_retirar <= 0:
            raise ValueError("El monto a retirar debe ser mayor que cero.")
        if cantidad_retirar > disponible:
            raise SaldoInsuficienteError(disponible, cantidad_retirar)

        self._saldo -= float(cantidad_retirar)

    def transferirDinero(self, cuenta_receptora: 'Cuenta', cantidad_transferir: float) -> None:
        """
        Transfiere dinero a otra cuenta receptora.
        Lanza SaldoInsuficienteError o ClienteEnMoraError si aplica.
        """
        if not isinstance(cuenta_receptora, Cuenta):
            raise TypeError("La cuenta receptora debe ser una instancia válida de Cuenta.")
        
        self.retirarDinero(cantidad_transferir)
        cuenta_receptora.ingresarDinero(cantidad_transferir)

    @abstractmethod
    def calcularInteres(self) -> float:
        """
        Método Polimórfico Abstracto: Cada subtipo implementa su propio cálculo de interés.
        """
        pass

    def __str__(self) -> str:
        return f"[{self._tipo.value}] N° {self._numero_cuenta} | Saldo: ${self._saldo:,.0f} | Titular: {self._titular.nombre}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(numero='{self._numero_cuenta}', saldo={self._saldo})"
