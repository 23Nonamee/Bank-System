from model.empleado import Empleado
from model.enums import TipoEmpleado, TipoCuenta
from model.rut import Rut
from model.cliente import Cliente
from model.cuenta import Cuenta
from model.cuenta_factory import CuentaFactory
from exceptions import ClienteEnMoraError

class Ejecutivo(Empleado):
    """
    Subtipo de Empleado: Ejecutivo bancario.
    """
    def __init__(self, nombre: str, rut: Rut, usuario: str, password: str):
        super().__init__(nombre, rut, TipoEmpleado.EJECUTIVO, usuario, password)

    def registrarCliente(self, nombre: str, rut_str: str) -> Cliente:
        """Registra un nuevo cliente en el sistema."""
        return Cliente(nombre=nombre, rut=Rut(rut_str))

    def agregarCuenta(self, cliente: Cliente, tipo_cuenta: TipoCuenta, numero_cuenta: str, **kwargs) -> Cuenta:
        """Crea y asigna una cuenta bancaria a un cliente usando CuentaFactory."""
        return CuentaFactory.crearCuenta(tipo_cuenta, cliente, numero_cuenta, **kwargs)

    def verificarMora(self, cliente: Cliente) -> bool:
        """Verifica si el cliente registra mora activa."""
        return cliente.tieneMoraVigente()

    def aprobarCredito(self, cuenta: Cuenta, monto: float) -> bool:
        """Aprueba un crédito si el cliente no está en mora."""
        if cuenta.titular.tieneMoraVigente():
            raise ClienteEnMoraError(cuenta.titular.nombre, cuenta.titular.mora_cliente.amount_mora)
        return True
