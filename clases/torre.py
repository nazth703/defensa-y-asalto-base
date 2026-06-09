# ============================================================
# torre.py - Clase Torre y sus tipos
# ============================================================

class Torre:
    """
    Clase base para todas las torres defensivas.
    Cada tipo de torre hereda de esta clase.
    """
    def __init__(self, nombre, costo, vida, danio, alcance, faccion="Medieval"):
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida
        self.vida = vida
        self.danio = danio
        self.alcance = alcance      #En casillas
        self.faccion = faccion
        self.fila = None
        self.columna = None
        self.turnos_habilidad = 3   #Turnos para activar habilidad
        self.contador_turnos = 0    #Contador actual

    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def esta_destruida(self):
        return self.vida <= 0

    def puede_atacar(self, fila_enemigo, col_enemigo):
        """Verifica si una unidad está dentro del alcance."""
        if self.fila is None or self.columna is None:
            return False
        distancia = abs(self.fila - fila_enemigo) + abs(self.columna - col_enemigo)
        return distancia <= self.alcance

    def atacar(self, unidad):
        """Ataca a una unidad y retorna el daño causado."""
        unidad.recibir_danio(self.danio)
        self.contador_turnos += 1
        return self.danio

    def habilidad_especial(self, unidades, torres):
        """Cada tipo de torre sobreescribe este método."""
        pass

    def habilidad_lista(self):
        return self.contador_turnos >= self.turnos_habilidad

    def __str__(self):
        return f"{self.nombre} [{self.faccion}] - Vida: {self.vida}/{self.vida_maxima} | Daño: {self.danio} | Alcance: {self.alcance}"


# ============================================================
# TIPO 1: Torre Básica
# Daño normal, costo bajo. Habilidad: Disparo doble
# ============================================================
class TorreBasica(Torre):
    def __init__(self, faccion="Medieval"):
        colores = {
            "Medieval":  {"costo": 50,  "vida": 100, "danio": 20, "alcance": 3},
            "Naturaleza": {"costo": 50, "vida": 90,  "danio": 22, "alcance": 3},
            "Oscura":    {"costo": 50,  "vida": 110, "danio": 18, "alcance": 3},
        }
        s = colores.get(faccion, colores["Medieval"])
        super().__init__("Torre Básica", s["costo"], s["vida"], s["danio"], s["alcance"], faccion)
        self.turnos_habilidad = 3

    def habilidad_especial(self, unidades, torres):
        """
        Disparo doble: ataca dos veces seguidas a la unidad más cercana.
        Retorna el daño extra causado.
        """
        if not unidades:
            return 0
        #Buscar la unidad más cercana dentro del alcance
        objetivo = None
        for u in unidades:
            if self.puede_atacar(u.fila, u.columna) and not u.esta_muerta():
                objetivo = u
                break
        if objetivo:
            objetivo.recibir_danio(self.danio)  #Segundo disparo
            self.contador_turnos = 0
            return self.danio
        return 0


# ============================================================
# TIPO 2: Torre Pesada
# Mucha vida y daño alto, costo elevado. Habilidad: Daño en área
# ============================================================
class TorrePesada(Torre):
    def __init__(self, faccion="Medieval"):
        stats = {
            "Medieval":  {"costo": 120, "vida": 300, "danio": 50, "alcance": 2},
            "Naturaleza": {"costo": 120, "vida": 280, "danio": 55, "alcance": 2},
            "Oscura":    {"costo": 120, "vida": 320, "danio": 45, "alcance": 2},
        }
        s = stats.get(faccion, stats["Medieval"])
        super().__init__("Torre Pesada", s["costo"], s["vida"], s["danio"], s["alcance"], faccion)
        self.turnos_habilidad = 4

    def habilidad_especial(self, unidades, torres):
        """
        Daño en área: daña a TODAS las unidades dentro del alcance.
        Retorna el daño total causado.
        """
        danio_total = 0
        for u in unidades:
            if self.puede_atacar(u.fila, u.columna) and not u.esta_muerta():
                u.recibir_danio(self.danio // 2)
                danio_total += self.danio // 2
        self.contador_turnos = 0
        return danio_total


# ============================================================
# TIPO 3: Torre Mágica
# Daño bajo, habilidad especial fuerte. Habilidad: Congelar unidad
# ============================================================
class TorreMagica(Torre):
    def __init__(self, faccion="Medieval"):
        stats = {
            "Medieval":  {"costo": 80, "vida": 80, "danio": 15, "alcance": 4},
            "Naturaleza": {"costo": 80, "vida": 75, "danio": 18, "alcance": 4},
            "Oscura":    {"costo": 80, "vida": 90,  "danio": 12, "alcance": 5},
        }
        s = stats.get(faccion, stats["Medieval"])
        super().__init__("Torre Mágica", s["costo"], s["vida"], s["danio"], s["alcance"], faccion)
        self.turnos_habilidad = 3

    def habilidad_especial(self, unidades, torres):
        """
        Congela la unidad más cercana por 2 turnos (velocidad = 0).
        Retorna True si congeló a alguien.
        """
        for u in unidades:
            if self.puede_atacar(u.fila, u.columna) and not u.esta_muerta() and not u.congelada:
                u.congelada = True
                u.turnos_congelada = 2
                self.contador_turnos = 0
                return True
        return False
