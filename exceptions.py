"""
Excepciones personalizadas del dominio bancario.
Requisito Rúbrica: Manejo de errores y excepciones del negocio.
"""

class DomainError(Exception):
    """Excepción base para todos los errores de dominio del sistema bancario."""
    pass


class RutInvalidoError(DomainError):
    """Lanzada cuando un RUT no cumple con el formato o el dígito verificador válido (Módulo 11)."""
    def __init__(self, rut: str, mensaje: str = "El RUT ingresado no es válido."):
        self.rut = rut
        self.mensaje = f"{mensaje} (RUT ingresado: '{rut}')"
        super().__init__(self.mensaje)


class SaldoInsuficienteError(DomainError):
    """Lanzada cuando se intenta realizar un retiro o transferencia que excede el saldo disponible."""
    def __init__(self, saldo_disponible: float, monto_solicitado: float):
        self.saldo_disponible = saldo_disponible
        self.monto_solicitado = monto_solicitado
        self.mensaje = (
            f"Operación rechazada: Saldo disponible insuficiente (${saldo_disponible:,.0f}) "
            f"para el monto solicitado (${monto_solicitado:,.0f})."
        )
        super().__init__(self.mensaje)


class ClienteEnMoraError(DomainError):
    """Lanzada cuando un cliente intenta realizar una operación restringida (apertura o giro) teniendo mora vigente."""
    def __init__(self, cliente_nombre: str, monto_mora: int):
        self.cliente_nombre = cliente_nombre
        self.monto_mora = monto_mora
        self.mensaje = (
            f"Operación bloqueada: El cliente '{cliente_nombre}' registra una mora vigente "
            f"de ${monto_mora:,.0f}."
        )
        super().__init__(self.mensaje)


class MontoInvalidoError(DomainError):
    """Lanzada cuando un monto ingresado no es válido (<= 0 o no numérico)."""
    def __init__(self, mensaje: str = "El monto debe ser un valor numérico positivo mayor a cero."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class EntidadNoEncontradaError(DomainError):
    """Lanzada cuando una entidad (Cliente, Cuenta, Transacción) no es encontrada en la base de datos."""
    def __init__(self, entidad: str, identificador: str):
        self.entidad = entidad
        self.identificador = identificador
        self.mensaje = f"No se encontró {entidad} con identificador '{identificador}'."
        super().__init__(self.mensaje)


class ApiIndicadorError(DomainError):
    """Excepción base para fallos al consultar la API externa de indicadores económicos."""
    pass


class ApiTimeoutError(ApiIndicadorError):
    """Lanzada cuando la solicitud a la API excede el tiempo de espera configurado."""
    pass


class ApiConexionError(ApiIndicadorError):
    """Lanzada cuando no es posible establecer conexión con el servicio externo (sin internet/red caída)."""
    pass
