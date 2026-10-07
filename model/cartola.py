from datetime import datetime
from typing import List, Optional
from model.cuenta import Cuenta
from model.movimiento import Movimiento

class Cartola:
    """
    Clase que representa la Cartola de Movimientos Bancarios (diagrama UML).
    """
    def __init__(self, cuenta: Cuenta, fecha_inicio: datetime, fecha_fin: datetime, movimientos: Optional[List[Movimiento]] = None):
        self._cuenta = cuenta
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._movimientos = movimientos if movimientos else []

    def generarCartola(self) -> str:
        """Genera y retorna la vista en texto de la cartola."""
        inicio_str = self._fecha_inicio.strftime("%d/%m/%Y")
        fin_str = self._fecha_fin.strftime("%d/%m/%Y")
        
        lineas = [
            "=" * 60,
            f"CARTOLA BANCARIA - CUENTA N° {self._cuenta.numero_cuenta}",
            f"Titular: {self._cuenta.titular.nombre} | RUT: {self._cuenta.titular.rut_cliente.getFormatedRut()}",
            f"Período: {inicio_str} al {fin_str}",
            f"Saldo Actual: ${self._cuenta.saldo:,.0f}",
            "-" * 60,
            "MOVIMIENTOS REGISTRADOS:"
        ]
        
        if not self._movimientos:
            lineas.append("  (No existen movimientos para el período seleccionado)")
        else:
            for idx, m in enumerate(self._movimientos, start=1):
                lineas.append(f"  {idx}. {m}")
                
        lineas.append("=" * 60)
        return "\n".join(lineas)

    def __str__(self) -> str:
        return self.generarCartola()
