# ============================================================
# ranking.py - Ventana de Top Jugadores
# ============================================================

import tkinter as tk
from clases.archivo_jugadores import obtener_top_defensores, obtener_top_atacantes

class VentanaRanking:
    """
    Ventana que muestra el top 5 de defensores y atacantes.
    """

    def __init__(self, root):
        self.ventana = tk.Toplevel(root)
        self.ventana.title("🏆 Ranking de Jugadores")
        self.ventana.geometry("450x500")
        self.ventana.configure(bg="#1a1a2e")
        self.ventana.resizable(False, False)
        self.construir_ui()

    def construir_ui(self):
        tk.Label(
            self.ventana,
            text="🏆 Top Jugadores",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        ).pack(pady=15)

        # ── Top Defensores ──
        tk.Label(
            self.ventana,
            text="🏰 Mejores Defensores",
            font=("Arial", 13, "bold"),
            bg="#1a1a2e",
            fg="#00ff88"
        ).pack(pady=(10, 5))

        frame_def = tk.Frame(self.ventana, bg="#16213e", pady=10, padx=20)
        frame_def.pack(padx=30, fill="x")

        defensores = obtener_top_defensores()
        if defensores:
            for i, j in enumerate(defensores, 1):
                tk.Label(
                    frame_def,
                    text=f"{i}. {j['usuario']}  —  {j['victorias_defensor']} victorias",
                    font=("Arial", 11),
                    bg="#16213e",
                    fg="white"
                ).pack(anchor="w", pady=2)
        else:
            tk.Label(frame_def, text="Sin registros aún", bg="#16213e",
                     fg="#aaaaaa", font=("Arial", 10)).pack()

        # ── Top Atacantes ──
        tk.Label(
            self.ventana,
            text="⚔️ Mejores Atacantes",
            font=("Arial", 13, "bold"),
            bg="#1a1a2e",
            fg="#ffaa00"
        ).pack(pady=(15, 5))

        frame_atk = tk.Frame(self.ventana, bg="#16213e", pady=10, padx=20)
        frame_atk.pack(padx=30, fill="x")

        atacantes = obtener_top_atacantes()
        if atacantes:
            for i, j in enumerate(atacantes, 1):
                tk.Label(
                    frame_atk,
                    text=f"{i}. {j['usuario']}  —  {j['victorias_atacante']} victorias",
                    font=("Arial", 11),
                    bg="#16213e",
                    fg="white"
                ).pack(anchor="w", pady=2)
        else:
            tk.Label(frame_atk, text="Sin registros aún", bg="#16213e",
                     fg="#aaaaaa", font=("Arial", 10)).pack()

        # Botón cerrar
        tk.Button(
            self.ventana,
            text="Cerrar",
            bg="#e94560",
            fg="white",
            relief="flat",
            font=("Arial", 11),
            padx=15, pady=5,
            command=self.ventana.destroy
        ).pack(pady=20)
