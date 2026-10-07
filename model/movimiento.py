from model.enums import TipoMovimiento
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from model.cuenta import Cuenta

class Movimiento:
    """
    Clase que representa una línea de detalle o movimiento individual de una transacción.
    Parte de la relación de Composición con Transaccion.
    """
    def __init__(
        self, 
        tipo: TipoMovimiento, 
        monto: float, 
        descripcion: str, 
        cuenta_origen: Optional['Cuenta'] = None, 
        cuenta_destino: Optional['Cuenta'] = None
    ):
        if not isinstance(tipo, TipoMovimiento):
            raise TypeError("El tipo de movimiento debe ser un TipoMovimiento (DEPOSITO, GIRO, TRANSFERENCIA).")
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto del movimiento debe ser un valor positivo.")
        
        self._tipo = tipo
        self._monto = float(monto)
        self._descripcion = str(descripcion).strip()
        self._cuenta_origen = cuenta_origen
        self._cuenta_destino = cuenta_destino

    @property
    def tipo(self) -> TipoMovimiento:
        return self._tipo

    @property
    def monto(self) -> float:
        return self._monto

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def cuenta_origen(self) -> Optional['Cuenta']:
        return self._cuenta_origen

    @property
    def cuenta_destino(self) -> Optional['Cuenta']:
        return self._cuenta_destino

    def __str__(self) -> str:
        origen_str = f" de N°{self._cuenta_origen.numero_cuenta}" if self._cuenta_origen else ""
        destino_str = f" a N°{self._cuenta_destino.numero_cuenta}" if self._cuenta_destino else ""
        return f"[{self._tipo.value}] ${self._monto:,.0f} - {self._descripcion}{origen_str}{destino_str}"

    def __repr__(self) -> str:
        return f"Movimiento(tipo={self._tipo.value}, monto={self._monto})"
