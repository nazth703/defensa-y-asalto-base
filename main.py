# ============================================================
# main.py - Archivo principal del juego
# ============================================================

import tkinter as tk
from clases.archivo_jugadores import inicializar_archivo
from ventanas.login import VentanaLogin
from ventanas.facciones import VentanaFacciones
from ventanas.mapa import VentanaMapa

def al_iniciar_sesion(jugador1, jugador2):
    """Se llama cuando ambos jugadores inician sesión."""
    VentanaFacciones(root, jugador1, jugador2, al_elegir_facciones)

def al_elegir_facciones(jugador1, faccion1, jugador2, faccion2):
    """Se llama cuando ambos eligen sus facciones."""
    VentanaMapa(root, jugador1, faccion1, jugador2, faccion2)

# ── Inicio del programa ──
if __name__ == "__main__":
    inicializar_archivo()           # Crea jugadores.json si no existe
    root = tk.Tk()
    root.withdraw()                 # Oculta la ventana principal vacía
    VentanaLogin(tk.Toplevel(root), al_iniciar_sesion)
    root.mainloop()