from enum import Enum

class TipoCuenta(Enum):
    """Tipos de cuenta soportados por el banco segun diagrama UML."""
    CORRIENTE = "CORRIENTE"
    AHORRO = "AHORRO"
    VISTA = "VISTA"


class TipoMovimiento(Enum):
    """Tipos de movimientos bancarios segun diagrama UML y guion de pruebas."""
    DEPOSITO = "DEPOSITO"
    GIRO = "GIRO"
    CARGO = "CARGO"
    TRANSFERENCIA = "TRANSFERENCIA"


class TipoEmpleado(Enum):
    """Tipos de empleados en el sistema."""
    EJECUTIVO = "EJECUTIVO"
    CAJERO = "CAJERO"
