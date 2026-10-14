from services.indicador_service import IndicadorService

class IndicadorDivisas:
    """
    Clase del Modelo UML para consumo de Indicadores Económicos.
    Delega en IndicadorService para mantener separación de responsabilidades.
    """
    @staticmethod
    def obtenerUF(timeout: float = 5.0) -> float:
        """Obtiene el valor de la UF en pesos chilenos."""
        return IndicadorService.obtener_uf(timeout=timeout)

    @staticmethod
    def obtenerDolar(timeout: float = 5.0) -> float:
        """Obtiene el valor del Dólar (USD) en pesos chilenos."""
        return IndicadorService.obtener_dolar(timeout=timeout)
