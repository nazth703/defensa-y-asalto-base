# ============================================================
# estructuras.py - Clases: Base Central y Muro
# ============================================================

class BaseCentral:
    """
    Representa la base central del defensor.
    Si es destruida, el atacante gana la ronda.
    """
    def __init__(self, faccion="Medieval"):
        self.vida_maxima = 500
        self.vida = 500
        self.faccion = faccion
        self.fila = 5      #Posición fija en el mapa (centro)
        self.columna = 5

    def recibir_danio(self, cantidad):
        """Reduce la vida de la base."""
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def esta_destruida(self):
        """Retorna True si la base fue destruida."""
        return self.vida <= 0

    def reparar(self):
        """Restaura la vida al máximo (entre rondas)."""
        self.vida = self.vida_maxima

    def __str__(self):
        return f"Base Central [{self.faccion}] - Vida: {self.vida}/{self.vida_maxima}"


class Muro:
    """
    Muro defensivo que bloquea el paso de unidades.
    No ataca, solo absorbe daño.
    """
    def __init__(self, faccion="Medieval"):
        self.nombre = "Muro"
        self.costo = 20
        self.faccion = faccion
        self.fila = None
        self.columna = None

        #Estadísticas según facción
        stats = {
            "Medieval": {"vida": 150, "color": "#8B4513"},
            "Naturaleza": {"vida": 120, "color": "#228B22"},
            "Oscura":    {"vida": 180, "color": "#2F2F2F"},
        }
        s = stats.get(faccion, stats["Medieval"])
        self.vida_maxima = s["vida"]
        self.vida = self.vida_maxima
        self.color = s["color"]

    def recibir_danio(self, cantidad):
        """Reduce la vida del muro."""
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def esta_destruido(self):
        return self.vida <= 0

    def __str__(self):
        return f"Muro [{self.faccion}] - Vida: {self.vida}/{self.vida_maxima}"
