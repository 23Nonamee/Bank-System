from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from model.enums import TipoMovimiento
from model.movimiento import Movimiento

if TYPE_CHECKING:
    from model.cuenta import Cuenta

class Transaccion:
    """
    Clase que representa una Transacción Bancaria.
    Relaciones UML:
    - Composición con Movimiento: La transacción posee y administra sus líneas de detalle.
    """
    def __init__(self, cuenta: 'Cuenta', fecha: Optional[datetime] = None):
        self._fecha = fecha if isinstance(fecha, datetime) else datetime.now()
        self._cuenta = cuenta
        self._detalles: List[Movimiento] = []

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def cuenta(self) -> 'Cuenta':
        return self._cuenta

    @property
    def detalles(self) -> List[Movimiento]:
        return list(self._detalles)

    def agregarDetalle(self, movimiento: Movimiento) -> None:
        """
        Agrega un objeto Movimiento existente a los detalles de la transacción.
        """
        if not isinstance(movimiento, Movimiento):
            raise TypeError("El detalle a agregar debe ser una instancia de Movimiento.")
        self._detalles.append(movimiento)

    def crearYAgregarDetalle(
        self, 
        tipo: TipoMovimiento, 
        monto: float, 
        descripcion: str, 
        cuenta_destino: Optional['Cuenta'] = None
    ) -> Movimiento:
        """
        Demuestra COMPOSICIÓN estricta: La transacción crea el detalle internamente.
        """
        movimiento = Movimiento(
            tipo=tipo,
            monto=monto,
            descripcion=descripcion,
            cuenta_origen=self._cuenta,
            cuenta_destino=cuenta_destino
        )
        self._detalles.append(movimiento)
        return movimiento

    def obtenerTipo(self) -> Optional[TipoMovimiento]:
        """Retorna el tipo predominante de movimiento en la transacción."""
        if self._detalles:
            return self._detalles[0].tipo
        return None

    def __str__(self) -> str:
        fecha_fmt = self._fecha.strftime("%d/%m/%Y %H:%M:%S")
        res = [f"Transacción [{fecha_fmt}] - Cuenta N° {self._cuenta.numero_cuenta}:"]
        for idx, det in enumerate(self._detalles, start=1):
            res.append(f"  {idx}. {det}")
        return "\n".join(res)

    def __repr__(self) -> str:
        return f"Transaccion(cuenta='{self._cuenta.numero_cuenta}', items={len(self._detalles)})"
