from model.rut import Rut
from model.enums import TipoEmpleado
import hashlib

class Empleado:
    """
    Clase Base que representa a un Empleado del banco.
    """
    def __init__(self, nombre: str, rut: Rut, tipo: TipoEmpleado, usuario: str, password: str):
        self._nombre = nombre
        self._rut = rut if isinstance(rut, Rut) else Rut(rut)
        self._tipo = tipo
        self._usuario = usuario
        self._passwordhash = self._hash_password(password)

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def iniciarSesion(self, usuario: str, password_hash_o_plain: str) -> bool:
        """Valida las credenciales de inicio de sesión."""
        h = self._hash_password(password_hash_o_plain) if len(password_hash_o_plain) != 64 else password_hash_o_plain
        return self._usuario == usuario and self._passwordhash == h

    def obtenerDatos(self) -> str:
        return f"Empleado: {self._nombre} ({self._tipo.value}) | RUT: {self._rut.getFormatedRut()}"

    def __str__(self) -> str:
        return self.obtenerDatos()
