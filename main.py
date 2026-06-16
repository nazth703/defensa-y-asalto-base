# ============================================================
# main.py - Archivo principal del juego
# ============================================================

import tkinter as tk
from clases.archivo_jugadores import inicializar_archivo
from ventanas.login import VentanaLogin
from ventanas.facciones import VentanaFacciones
from ventanas.roles import VentanaRoles
from ventanas.mapa import VentanaMapa

def al_iniciar_sesion(jugador1, jugador2):
    """Se llama cuando ambos jugadores inician sesión."""
    VentanaFacciones(root, jugador1, jugador2, al_elegir_facciones)

def al_elegir_facciones(jugador1, faccion1, jugador2, faccion2):
    """Se llama cuando ambos eligen sus facciones."""
    VentanaRoles(root, jugador1, faccion1, jugador2, faccion2, al_elegir_roles)

def al_elegir_roles(defensor, faccion_def, atacante, faccion_atk):
    """Se llama cuando ambos eligen sus roles."""
    VentanaMapa(root, defensor, faccion_def, atacante, faccion_atk)

# ── Inicio del programa ──
if __name__ == "__main__":
    inicializar_archivo()
    root = tk.Tk()
    root.withdraw()
    VentanaLogin(tk.Toplevel(root), al_iniciar_sesion)
    root.mainloop()