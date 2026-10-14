import json
import requests
from exceptions import ApiIndicadorError, ApiTimeoutError, ApiConexionError

class IndicadorService:
    """
    Servicio centralizado para el consumo de indicadores económicos externos (mindicador.cl).
    Cumple con el Criterio 3.1: librería requests, timeout explícito y excepciones específicas.
    """
    URL_UF = "https://mindicador.cl/api/uf"
    URL_DOLAR = "https://mindicador.cl/api/dolar"

    @classmethod
    def _consultar_api(cls, url: str, clave_indicador: str, timeout: float = 5.0) -> float:
        """
        Realiza la petición HTTP con control riguroso de errores y timeouts.
        Captura de forma específica Timeout, ConnectionError, HTTPError y errores de estructura.
        """
        headers = {"User-Agent": "SouthPark-Bank/1.0 (Python/Requests)"}
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout as ex:
            raise ApiTimeoutError(f"Tiempo de espera agotado ({timeout}s) al consultar la API externa ({url}).") from ex
        except requests.exceptions.ConnectionError as ex:
            raise ApiConexionError("Error de conexión: No se pudo conectar al servicio mindicador.cl (verifique su conexión a internet).") from ex
        except requests.exceptions.HTTPError as ex:
            raise ApiIndicadorError(f"Error HTTP del servidor externo ({response.status_code}): {ex}") from ex
        except requests.exceptions.RequestException as ex:
            raise ApiIndicadorError(f"Error de red al consultar el servicio externo: {ex}") from ex
        except json.JSONDecodeError as ex:
            raise ApiIndicadorError("La respuesta del servicio externo no posee un formato JSON válido.") from ex

        try:
            # mindicador.cl devuelve { ..., "serie": [ {"fecha": "...", "valor": 37800.5}, ... ] }
            serie = data["serie"]
            if not serie or not isinstance(serie, list):
                raise ValueError("La lista de serie histórica está vacía.")
            valor = serie[0]["valor"]
            return float(valor)
        except (KeyError, IndexError, TypeError, ValueError) as ex:
            raise ApiIndicadorError(f"Estructura inesperada en la respuesta de la API para '{clave_indicador}': {ex}") from ex

    @classmethod
    def obtener_uf(cls, timeout: float = 5.0) -> float:
        """Obtiene el valor oficial de la Unidad de Fomento (UF) para la fecha actual."""
        return cls._consultar_api(cls.URL_UF, "uf", timeout=timeout)

    @classmethod
    def obtener_dolar(cls, timeout: float = 5.0) -> float:
        """Obtiene el valor oficial del Dólar Observado (USD) para la fecha actual."""
        return cls._consultar_api(cls.URL_DOLAR, "dolar", timeout=timeout)
