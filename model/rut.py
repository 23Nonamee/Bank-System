import re
from exceptions import RutInvalidoError

class Rut:
    """
    Clase que representa y valida un RUT chileno.
    Encapsulamiento: Atributo privado _identificador con @property y setter validado.
    """
    def __init__(self, identificador: str):
        self._identificador = None
        self.identificador = identificador  # Invoca el setter para validar

    @property
    def identificador(self) -> str:
        return self._identificador

    @identificador.setter
    def identificador(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise RutInvalidoError(str(valor), "El RUT debe ser una cadena de texto no vacía.")
        
        rut_limpio = valor.replace(".", "").replace("-", "").strip().upper()
        if not self._validar_rut_chileno(rut_limpio):
            raise RutInvalidoError(valor, "Dígito verificador de RUT no válido segun Modulo 11.")
        
        self._identificador = rut_limpio

    @staticmethod
    def _validar_rut_chileno(rut_limpio: str) -> bool:
        if len(rut_limpio) < 2:
            return False
        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]
        
        if not cuerpo.isdigit():
            return False

        # Algoritmo Módulo 11
        suma = 0
        multiplicador = 2
        for c in reversed(cuerpo):
            suma += int(c) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = suma % 11
        dv_calculado = 11 - resto
        if dv_calculado == 11:
            dv_esperado = '0'
        elif dv_calculado == 10:
            dv_esperado = 'K'
        else:
            dv_esperado = str(dv_calculado)

        return dv == dv_esperado

    def validateRut(self) -> bool:
        """Método requerido por el diagrama UML para validar el RUT."""
        try:
            return self._validar_rut_chileno(self._identificador)
        except Exception:
            return False

    def getRut(self) -> str:
        """Devuelve el RUT limpio sin puntos ni guion."""
        return self._identificador

    def getFormatedRut(self) -> str:
        """Devuelve el RUT formateado (ejemplo: 12.345.678-K)."""
        if not self._identificador:
            return ""
        cuerpo = self._identificador[:-1]
        dv = self._identificador[-1]
        
        # Formatear cuerpo con puntos
        cuerpo_fmt = f"{int(cuerpo):,}".replace(",", ".")
        return f"{cuerpo_fmt}-{dv}"

    def __str__(self) -> str:
        return self.getFormatedRut()

    def __repr__(self) -> str:
        return f"Rut('{self.getFormatedRut()}')"
