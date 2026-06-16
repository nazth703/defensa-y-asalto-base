# ============================================================
# roles.py - Ventana de Selección de Roles
# ============================================================

import tkinter as tk
from tkinter import messagebox

class VentanaRoles:
    """
    Ventana donde cada jugador elige si quiere ser defensor o atacante.
    No pueden elegir el mismo rol.
    """

    def __init__(self, root, jugador1, faccion1, jugador2, faccion2, callback):
        self.root = root
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.faccion1 = faccion1
        self.faccion2 = faccion2
        self.callback = callback
        self.rol1 = tk.StringVar(value="")
        self.rol2 = tk.StringVar(value="")

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Selección de Roles")
        self.ventana.geometry("520x480")
        self.ventana.configure(bg="#1a1a2e")
        self.ventana.resizable(False, False)
        self.ventana.grab_set()

        self.construir_ui()

    def construir_ui(self):
        tk.Label(
            self.ventana,
            text="⚔️ Elige tu Rol ⚔️",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e", fg="#e94560"
        ).pack(pady=15)

        tk.Label(
            self.ventana,
            text="El defensor construye torres y protege su base.\nEl atacante envía unidades a destruirla.",
            font=("Arial", 9),
            bg="#1a1a2e", fg="#aaaaaa",
            justify="center"
        ).pack(pady=(0, 15))

        frame_principal = tk.Frame(self.ventana, bg="#1a1a2e")
        frame_principal.pack(fill="both", expand=True, padx=20)

        self._crear_columna(frame_principal, self.jugador1["usuario"], self.faccion1, self.rol1, 0)

        tk.Frame(frame_principal, bg="#e94560", width=2).grid(
            row=0, column=1, sticky="ns", padx=10, pady=10
        )

        self._crear_columna(frame_principal, self.jugador2["usuario"], self.faccion2, self.rol2, 2)

        tk.Button(
            self.ventana,
            text="✅ Confirmar y Jugar",
            font=("Arial", 13, "bold"),
            bg="#e94560", fg="white",
            activebackground="#c73652",
            relief="flat", padx=20, pady=10,
            command=self.confirmar
        ).pack(pady=20)

    def _crear_columna(self, parent, nombre, faccion, var_rol, columna):
        frame = tk.Frame(parent, bg="#1a1a2e")
        frame.grid(row=0, column=columna, padx=10, pady=10, sticky="n")

        tk.Label(
            frame, text=nombre,
            font=("Arial", 13, "bold"),
            bg="#1a1a2e", fg="#00ff88"
        ).pack(pady=(0, 5))

        tk.Label(
            frame, text=f"Facción: {faccion}",
            font=("Arial", 9),
            bg="#1a1a2e", fg="#aaaaaa"
        ).pack(pady=(0, 15))

        # Botón defensor
        frame_def = tk.Frame(frame, bg="#0f3460", pady=15, padx=10)
        frame_def.pack(fill="x", pady=5)

        tk.Radiobutton(
            frame_def,
            text="🏰 Defensor",
            variable=var_rol,
            value="defensor",
            font=("Arial", 12, "bold"),
            bg="#0f3460", fg="#00ff88",
            selectcolor="#0f3460",
            activebackground="#0f3460"
        ).pack(anchor="w")

        tk.Label(
            frame_def,
            text="Construye torres y muros\npara proteger tu base.",
            font=("Arial", 8),
            bg="#0f3460", fg="#aaaaaa",
            justify="left"
        ).pack(anchor="w", padx=20)

        # Botón atacante
        frame_atk = tk.Frame(frame, bg="#3d0a0a", pady=15, padx=10)
        frame_atk.pack(fill="x", pady=5)

        tk.Radiobutton(
            frame_atk,
            text="⚔️ Atacante",
            variable=var_rol,
            value="atacante",
            font=("Arial", 12, "bold"),
            bg="#3d0a0a", fg="#e94560",
            selectcolor="#3d0a0a",
            activebackground="#3d0a0a"
        ).pack(anchor="w")

        tk.Label(
            frame_atk,
            text="Envía soldados, tanques\ny unidades rápidas.",
            font=("Arial", 8),
            bg="#3d0a0a", fg="#aaaaaa",
            justify="left"
        ).pack(anchor="w", padx=20)

    def confirmar(self):
        r1 = self.rol1.get()
        r2 = self.rol2.get()

        if not r1:
            messagebox.showwarning("Falta", f"{self.jugador1['usuario']} debe elegir un rol")
            return
        if not r2:
            messagebox.showwarning("Falta", f"{self.jugador2['usuario']} debe elegir un rol")
            return
        if r1 == r2:
            messagebox.showwarning("Error", "¡Los jugadores no pueden tener el mismo rol!")
            return

        self.ventana.destroy()

        # Ordenar: defensor primero, atacante segundo
        if r1 == "defensor":
            self.callback(
                self.jugador1, self.faccion1,
                self.jugador2, self.faccion2
            )
        else:
            self.callback(
                self.jugador2, self.faccion2,
                self.jugador1, self.faccion1
            )