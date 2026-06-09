# ============================================================
# facciones.py - Ventana de Selección de Facciones
# ============================================================

import tkinter as tk
from tkinter import messagebox

# Información visual de cada facción
FACCIONES = {
    "Medieval": {
        "emoji": "🏰",
        "color": "#8B4513",
        "descripcion": "Muros de piedra y torres de arqueros.\nFuertes y resistentes.",
        "bg": "#3d1f0a"
    },
    "Naturaleza": {
        "emoji": "🌿",
        "color": "#228B22",
        "descripcion": "Trampas de raíces y torres de druidas.\nVeloces y ágiles.",
        "bg": "#0a3d0a"
    },
    "Oscura": {
        "emoji": "💀",
        "color": "#6a0dad",
        "descripcion": "Muros de obsidiana y torres de sombras.\nAlta resistencia.",
        "bg": "#1a0a2e"
    }
}

class VentanaFacciones:
    """
    Ventana donde cada jugador elige su facción.
    No pueden elegir la misma facción.
    """

    def __init__(self, root, jugador1, jugador2, callback):
        """
        jugador1, jugador2: diccionarios con datos de los jugadores
        callback: función que recibe (jugador1, faccion1, jugador2, faccion2)
        """
        self.root = root
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.callback = callback
        self.faccion1 = tk.StringVar(value="")
        self.faccion2 = tk.StringVar(value="")

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Selección de Facciones")
        self.ventana.geometry("580x620")
        self.ventana.configure(bg="#1a1a2e")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()  # Bloquea la ventana anterior

        self.construir_ui()

    def construir_ui(self):
        tk.Label(
            self.ventana,
            text="⚔️ Elige tu Facción ⚔️",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        ).pack(pady=15)

        # Frame para ambos jugadores lado a lado
        frame_principal = tk.Frame(self.ventana, bg="#1a1a2e")
        frame_principal.pack(fill="both", expand=True, padx=20)

        # Columna jugador 1
        self._crear_columna_jugador(
            frame_principal,
            self.jugador1["usuario"],
            self.faccion1,
            columna=0
        )

        # Separador
        tk.Frame(frame_principal, bg="#e94560", width=2).grid(
            row=0, column=1, sticky="ns", padx=10, pady=10
        )

        # Columna jugador 2
        self._crear_columna_jugador(
            frame_principal,
            self.jugador2["usuario"],
            self.faccion2,
            columna=2
        )

        # Botón confirmar
        tk.Button(
            self.ventana,
            text="✅ Confirmar y Continuar",
            font=("Arial", 13, "bold"),
            bg="#e94560",
            fg="white",
            activebackground="#c73652",
            relief="flat",
            padx=20, pady=10,
            command=self.confirmar
        ).pack(pady=20)

    def _crear_columna_jugador(self, parent, nombre, var_faccion, columna):
        """Crea la columna de selección de facción para un jugador."""
        frame = tk.Frame(parent, bg="#1a1a2e")
        frame.grid(row=0, column=columna, padx=10, pady=10, sticky="n")

        tk.Label(
            frame,
            text=nombre,
            font=("Arial", 13, "bold"),
            bg="#1a1a2e",
            fg="#00ff88"
        ).pack(pady=(0, 10))

        for nombre_faccion, datos in FACCIONES.items():
            self._crear_boton_faccion(frame, nombre_faccion, datos, var_faccion)

    def _crear_boton_faccion(self, parent, nombre_faccion, datos, var_faccion):
        """Crea un botón de selección para una facción."""
        frame_btn = tk.Frame(parent, bg=datos["bg"], pady=8, padx=10)
        frame_btn.pack(fill="x", pady=5)

        tk.Radiobutton(
            frame_btn,
            text=f"{datos['emoji']} {nombre_faccion}",
            variable=var_faccion,
            value=nombre_faccion,
            font=("Arial", 12, "bold"),
            bg=datos["bg"],
            fg=datos["color"],
            selectcolor=datos["bg"],
            activebackground=datos["bg"],
        ).pack(anchor="w")

        tk.Label(
            frame_btn,
            text=datos["descripcion"],
            font=("Arial", 8),
            bg=datos["bg"],
            fg="#cccccc",
            justify="left"
        ).pack(anchor="w", padx=20)

    def confirmar(self):
        """Valida la selección y llama al callback."""
        f1 = self.faccion1.get()
        f2 = self.faccion2.get()

        if not f1:
            messagebox.showwarning("Falta", f"{self.jugador1['usuario']} debe elegir una facción")
            return
        if not f2:
            messagebox.showwarning("Falta", f"{self.jugador2['usuario']} debe elegir una facción")
            return
        if f1 == f2:
            messagebox.showwarning("Error", "¡Los jugadores no pueden elegir la misma facción!")
            return

        self.ventana.destroy()
        self.callback(self.jugador1, f1, self.jugador2, f2)
