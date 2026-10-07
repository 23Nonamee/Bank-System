"""
Excepciones personalizadas del dominio bancario.
Requisito Rúbrica 2.1.4: Manejo de errores y excepciones del negocio.
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
    """Lanzada cuando un cliente intenta realizar una operación restringida teniendo mora vigente."""
    def __init__(self, cliente_nombre: str, monto_mora: int):
        self.cliente_nombre = cliente_nombre
        self.monto_mora = monto_mora
        self.mensaje = (
            f"Operación bloqueada: El cliente '{cliente_nombre}' registra una mora vigente "
            f"de ${monto_mora:,.0f}."
        )
        super().__init__(self.mensaje)
