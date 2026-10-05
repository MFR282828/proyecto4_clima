from abc import ABC, abstractmethod


class LecturaClimaticaBase(ABC):
    """CLASE ABSTRACTA (POO): Funciona como la plantilla o contrato obligatorio.

    Cualquier lectura de clima en el futuro DEBE heredar de esta clase.
    """

    def __init__(self, ciudad: str, humedad: float):
        self.ciudad = ciudad
        self.humedad = humedad

    @abstractmethod
    def calcular_nivel_riesgo(self) -> str:
        """Método Abstracto: Obliga a las clases hijas a implementar su propia lógica de riesgo."""
        pass


class LecturaTemperatura(LecturaClimaticaBase):
    """CLASE HIJA (POO): Procesa lecturas de temperatura aplicando Programación Defensiva

    para proteger la integridad de los datos financieros/climáticos.
    """

    def __init__(self, ciudad: str, humedad: float, temperatura_celsius: float):
        # Invocamos el constructor de la clase padre (LecturaClimaticaBase)
        super().__init__(ciudad, humedad)

        # AQUÍ OCURRE LA MAGIA: Al asignar self.temperatura, Python llama automáticamente
        # al @temperatura.setter de abajo para validar el dato antes de guardarlo.
        self.temperatura = temperatura_celsius

    # ------------------------------------------------------------------
    # ADUANA DE SEGURIDAD (Encapsulamiento con @property y @setter)
    # ------------------------------------------------------------------

    @property
    def temperatura(self) -> float:
        """GETTER: Permite LEER la variable protegida '_temperatura' de forma limpia."""
        return self._temperatura

    @temperatura.setter
    def temperatura(self, valor: float):
        """SETTER: Intercepta y valida cualquier intento de modificación."""
        # 1. Validación de Tipo (Evita ataques o errores de datos corruptos desde la API)
        if not isinstance(valor, (int, float)):
            raise TypeError(
                "[ERROR DE SEGURIDAD] La temperatura debe ser un número real."
            )

        # 2. Validación de Rango Físico (Límite biológico/geográfico razonable en la Tierra)
        if valor < -90.0 or valor > 60.0:
            raise ValueError(
                f"[ERROR DE DATOS] Temperatura de {valor}°C fuera de límites físicos habidos."
            )

        # Si supera todas las pruebas de seguridad, se guarda en el atributo protegido '_temperatura'
        self._temperatura = float(valor)

    # ------------------------------------------------------------------
    # REGLA DE NEGOCIO (Dominio del Proyecto)
    # ------------------------------------------------------------------

    def calcular_nivel_riesgo(self) -> str:
        """Calcula el riesgo de helada o calor extremo según la temperatura validada."""
        if self._temperatura <= 0.0:
            return "ALERTA_HELADA (Riesgo Agrícola)"
        elif self._temperatura >= 35.0:
            return "ALERTA_OLA_DE_CALOR (Riesgo de Salud/Incendio)"
        else:
            return "CONDICION_NORMAL"

    def __str__(self) -> str:
        """Formato visual representativo para consola."""
        return f"[{self.ciudad}] Temp: {self.temperatura}°C | Humedad: {self.humedad}% | Estado: {self.calcular_nivel_riesgo()}"