# ============================================================
# unidad.py - Clase Unidad y sus tipos
# ============================================================

class Unidad:
    """
    Clase base para todas las unidades atacantes.
    Las unidades avanzan por el mapa hacia la base central.
    """
    def __init__(self, nombre, costo, vida, danio, velocidad, faccion="Medieval"):
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida
        self.vida = vida
        self.danio = danio
        self.velocidad = velocidad      #Casillas que avanza por turno
        self.faccion = faccion
        self.fila = None
        self.columna = None
        self.turnos_habilidad = 3
        self.contador_turnos = 0
        self.congelada = False          #Estado: congelada por torre mágica
        self.turnos_congelada = 0

    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def esta_muerta(self):
        return self.vida <= 0

    def mover(self, mapa):
        """
        Avanza hacia la base central.
        Retorna True si llegó a la base.
        """
        if self.congelada:
            self.turnos_congelada -= 1
            if self.turnos_congelada <= 0:
                self.congelada = False
            return False

        #Avanzar hacia la izquierda (columna menor = base central)
        pasos = self.velocidad
        while pasos > 0 and self.columna > 0:
            self.columna -= 1
            pasos -= 1

        self.contador_turnos += 1
        return self.columna == 0  #Llegó a la base

    def atacar_torre(self, torre):
        """Ataca a una torre."""
        torre.recibir_danio(self.danio)
        return self.danio

    def atacar_base(self, base):
        """Ataca la base central."""
        base.recibir_danio(self.danio)
        return self.danio

    def habilidad_especial(self, torres, base):
        """Cada tipo sobreescribe este método."""
        pass

    def habilidad_lista(self):
        return self.contador_turnos >= self.turnos_habilidad

    def __str__(self):
        return f"{self.nombre} [{self.faccion}] - Vida: {self.vida}/{self.vida_maxima} | Daño: {self.danio} | Vel: {self.velocidad}"


# ============================================================
# TIPO 1: Soldado
# Bajo costo, estadísticas normales. Habilidad: Ataque doble
# ============================================================
class Soldado(Unidad):
    def __init__(self, faccion="Medieval"):
        stats = {
            "Medieval":  {"costo": 30, "vida": 80,  "danio": 15, "velocidad": 1},
            "Naturaleza": {"costo": 30, "vida": 75,  "danio": 17, "velocidad": 1},
            "Oscura":    {"costo": 30, "vida": 90,  "danio": 13, "velocidad": 1},
        }
        s = stats.get(faccion, stats["Medieval"])
        super().__init__("Soldado", s["costo"], s["vida"], s["danio"], s["velocidad"], faccion)
        self.turnos_habilidad = 3

    def habilidad_especial(self, torres, base):
        """
        Ataque doble: golpea dos veces al objetivo más cercano.
        """
        #Buscar torre en la misma casilla o adyacente
        for torre in torres:
            if torre.fila == self.fila and abs(torre.columna - self.columna) <= 1:
                torre.recibir_danio(self.danio)  # Segundo golpe
                self.contador_turnos = 0
                return self.danio
        #Si no hay torre, golpea la base
        if self.columna == 0:
            base.recibir_danio(self.danio)
            self.contador_turnos = 0
            return self.danio
        return 0


# ============================================================
# TIPO 2: Tanque
# Mucha vida, movimiento lento. Habilidad: Escudo temporal
# ============================================================
class Tanque(Unidad):
    def __init__(self, faccion="Medieval"):
        stats = {
            "Medieval":  {"costo": 100, "vida": 300, "danio": 30, "velocidad": 1},
            "Naturaleza": {"costo": 100, "vida": 280, "danio": 33, "velocidad": 1},
            "Oscura":    {"costo": 100, "vida": 320, "danio": 27, "velocidad": 1},
        }
        s = stats.get(faccion, stats["Medieval"])
        super().__init__("Tanque", s["costo"], s["vida"], s["danio"], s["velocidad"], faccion)
        self.turnos_habilidad = 4
        self.escudo_activo = False

    def recibir_danio(self, cantidad):
        """Si el escudo está activo, reduce el daño a la mitad."""
        if self.escudo_activo:
            cantidad = cantidad // 2
        super().recibir_danio(cantidad)

    def habilidad_especial(self, torres, base):
        """
        Escudo temporal: reduce el daño recibido a la mitad por 2 turnos.
        """
        self.escudo_activo = True
        self.contador_turnos = 0
        #El escudo dura 2 turnos, se desactiva en mover()
        return True


# ============================================================
# TIPO 3: Unidad Rápida
# Poco daño, se mueve más rápido. Habilidad: Aumento de velocidad
# ============================================================
class UnidadRapida(Unidad):
    def __init__(self, faccion="Medieval"):
        stats = {
            "Medieval":  {"costo": 50, "vida": 60,  "danio": 10, "velocidad": 2},
            "Naturaleza": {"costo": 50, "vida": 55,  "danio": 12, "velocidad": 2},
            "Oscura":    {"costo": 50, "vida": 70,  "danio": 8,  "velocidad": 2},
        }
        s = stats.get(faccion, stats["Medieval"])
        super().__init__("Unidad Rápida", s["costo"], s["vida"], s["danio"], s["velocidad"], faccion)
        self.turnos_habilidad = 2
        self.boost_activo = False

    def habilidad_especial(self, torres, base):
        """
        Aumento de velocidad: se mueve 3 casillas en lugar de 2 por 1 turno.
        """
        self.velocidad = 3
        self.boost_activo = True
        self.contador_turnos = 0
        return True

    def mover(self, mapa):
        resultado = super().mover(mapa)
        #Desactivar boost después de usarlo
        if self.boost_activo:
            self.velocidad = 2
            self.boost_activo = False
        return resultado
