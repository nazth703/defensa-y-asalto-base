# ============================================================
# jugador.py - Clase Jugador
# ============================================================

class Jugador:
    """
    Representa a un jugador del juego.
    Guarda su información, victorias y dinero actual.
    """
    def __init__(self, usuario, contrasena):
        self.usuario = usuario
        self.contrasena = contrasena
        self.victorias_defensor = 0
        self.victorias_atacante = 0

        #Estado durante la partida
        self.dinero = 0
        self.faccion = None
        self.rol = None         #"defensor" o "atacante"
        self.rondas_ganadas = 0

    def dar_dinero(self, cantidad):
        self.dinero += cantidad

    def gastar_dinero(self, cantidad):
        """Retorna True si pudo gastar, False si no tiene suficiente."""
        if self.dinero >= cantidad:
            self.dinero -= cantidad
            return True
        return False

    def tiene_dinero(self, cantidad):
        return self.dinero >= cantidad

    def ganar_ronda(self):
        self.rondas_ganadas += 1

    def ganar_partida(self):
        """Suma una victoria según el rol que jugó."""
        if self.rol == "defensor":
            self.victorias_defensor += 1
        elif self.rol == "atacante":
            self.victorias_atacante += 1

    def resetear_para_partida(self):
        """Reinicia el estado del jugador para una nueva partida."""
        self.dinero = 0
        self.rondas_ganadas = 0

    def to_dict(self):
        """Convierte el jugador a diccionario para guardar en JSON."""
        return {
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante
        }

    @staticmethod
    def from_dict(datos):
        """Crea un Jugador desde un diccionario (leído del JSON)."""
        j = Jugador(datos["usuario"], datos["contrasena"])
        j.victorias_defensor = datos.get("victorias_defensor", 0)
        j.victorias_atacante = datos.get("victorias_atacante", 0)
        return j

    def __str__(self):
        return (f"Jugador: {self.usuario} | "
                f"Victorias defensor: {self.victorias_defensor} | "
                f"Victorias atacante: {self.victorias_atacante}")
