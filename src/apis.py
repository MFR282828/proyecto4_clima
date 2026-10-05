from typing import Optional, Tuple
import requests
from src.models import LecturaTemperatura


class ClienteAPIClima:
    """CLIENTE DE INFRAESTRUCTURA: Gestiona la comunicación con APIs de geocodificación y clima."""

    URL_CLIMA = "https://api.open-meteo.com/v1/forecast"
    URL_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"

    def __init__(self, timeout_segundos: int = 10):
        self.timeout = timeout_segundos

    def obtener_coordenadas(self, ciudad: str) -> Optional[Tuple[float, float]]:
        """GEOCODIFICACIÓN: Convierte el nombre de una ciudad (ej. 'Lima')

        en sus coordenadas reales (latitud, longitud) usando la API de búsqueda.
        """
        parametros = {"name": ciudad, "count": 1, "language": "es", "format": "json"}

        try:
            respuesta = requests.get(
                self.URL_GEOCODING, params=parametros, timeout=self.timeout
            )
            respuesta.raise_for_status()
            datos = respuesta.json()

            # Verificamos si la API encontró resultados para el nombre ingresado
            if "results" in datos and len(datos["results"]) > 0:
                primer_resultado = datos["results"][0]
                lat = float(primer_resultado["latitude"])
                lon = float(primer_resultado["longitude"])
                return lat, lon

            print(
                f"[ADVERTENCIA] No se encontraron coordenadas para la ciudad '{ciudad}'."
            )
            return None

        except requests.exceptions.RequestException as e:
            print(f"[ERROR DE RED] Error al geocodificar '{ciudad}': {e}")
            return None

    def obtener_clima_por_ciudad(
        self, ciudad: str
    ) -> Optional[LecturaTemperatura]:
        """Flujo Completo:

        1. Convierte el nombre de la ciudad a coordenadas (lat, lon).
        2. Consulta la API del clima con esas coordenadas.
        3. Construye y retorna el objeto 'LecturaTemperatura' protegido por POO.
        """
        # Paso 1: Cambio de formato (Texto -> Coordenadas)
        coordenadas = self.obtener_coordenadas(ciudad)
        if not coordenadas:
            return None

        latitud, longitud = coordenadas

        # Paso 2: Consulta de clima con coordenadas
        parametros = {
            "latitude": latitud,
            "longitude": longitud,
            "current_weather": "true",
        }

        try:
            respuesta = requests.get(
                self.URL_CLIMA, params=parametros, timeout=self.timeout
            )
            respuesta.raise_for_status()
            datos = respuesta.json()

            temp_actual = float(datos["current_weather"]["temperature"])

            # Paso 3: Retorno del modelo de negocio validado por @setter
            return LecturaTemperatura(
                ciudad=ciudad.capitalize(),
                humedad=70.0,  # Valor simulado
                temperatura_celsius=temp_actual,
            )

        except requests.exceptions.RequestException as e:
            print(f"[ERROR DE RED] No se pudo obtener el clima: {e}")
            return None
        except (ValueError, TypeError) as e:
            print(f"[ERROR DE VALIDACION] Datos de la API corruptos: {e}")
            return None