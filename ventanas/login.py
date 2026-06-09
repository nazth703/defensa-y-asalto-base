# ============================================================
# login.py - Ventana de Login y Registro
# ============================================================

import tkinter as tk
from tkinter import messagebox
from clases.archivo_jugadores import registrar_jugador, iniciar_sesion

class VentanaLogin:
    """
    Ventana de inicio de sesión y registro.
    Permite a los dos jugadores iniciar sesión antes de jugar.
    """

    def __init__(self, root, callback_inicio):
        """
        root: ventana principal de Tkinter
        callback_inicio: función que se llama cuando ambos jugadores inician sesión
        """
        self.root = root
        self.callback_inicio = callback_inicio
        self.jugador1 = None
        self.jugador2 = None

        self.root.title("Defensa y Asalto de Base")
        self.root.geometry("500x600")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        self.construir_ui()

    def construir_ui(self):
        """Construye toda la interfaz de la ventana."""

        # Título del juego
        tk.Label(
            self.root,
            text="⚔️ Defensa y Asalto de Base ⚔️",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        ).pack(pady=20)

        # ── JUGADOR 1 ──
        self.frame_j1 = self._crear_frame_jugador("Jugador 1", "#16213e")
        self.frame_j1.pack(padx=30, pady=10, fill="x")

        # ── JUGADOR 2 ──
        self.frame_j2 = self._crear_frame_jugador("Jugador 2", "#16213e")
        self.frame_j2.pack(padx=30, pady=10, fill="x")

        # ── Botón iniciar ──
        tk.Button(
            self.root,
            text="🎮 Iniciar Partida",
            font=("Arial", 13, "bold"),
            bg="#e94560",
            fg="white",
            activebackground="#c73652",
            relief="flat",
            padx=20,
            pady=10,
            command=self.iniciar_partida
        ).pack(pady=20)

        # ── Botón ver ranking ──
        tk.Button(
            self.root,
            text="🏆 Ver Ranking",
            font=("Arial", 11),
            bg="#0f3460",
            fg="white",
            activebackground="#0a2a50",
            relief="flat",
            padx=15,
            pady=7,
            command=self.ver_ranking
        ).pack()

    def _crear_frame_jugador(self, titulo, color_fondo):
        """Crea el frame de login/registro para un jugador."""
        frame = tk.Frame(self.root, bg=color_fondo, pady=10, padx=15)

        tk.Label(
            frame,
            text=titulo,
            font=("Arial", 13, "bold"),
            bg=color_fondo,
            fg="#e94560"
        ).grid(row=0, column=0, columnspan=3, pady=(0, 8))

        # Usuario
        tk.Label(frame, text="Usuario:", bg=color_fondo, fg="white",
                 font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5)
        entry_usuario = tk.Entry(frame, font=("Arial", 10), width=20)
        entry_usuario.grid(row=1, column=1, padx=5, pady=3)

        # Contraseña
        tk.Label(frame, text="Contraseña:", bg=color_fondo, fg="white",
                 font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5)
        entry_contrasena = tk.Entry(frame, font=("Arial", 10), width=20, show="*")
        entry_contrasena.grid(row=2, column=1, padx=5, pady=3)

        # Label de estado
        label_estado = tk.Label(frame, text="", bg=color_fondo,
                                font=("Arial", 9), fg="#aaaaaa")
        label_estado.grid(row=3, column=0, columnspan=3, pady=3)

        # Botones
        btn_login = tk.Button(
            frame, text="Iniciar Sesión",
            bg="#0f3460", fg="white", relief="flat",
            font=("Arial", 9),
            command=lambda: self._login(titulo, entry_usuario, entry_contrasena, label_estado)
        )
        btn_login.grid(row=4, column=0, padx=5, pady=5)

        btn_registro = tk.Button(
            frame, text="Registrarse",
            bg="#533483", fg="white", relief="flat",
            font=("Arial", 9),
            command=lambda: self._registro(entry_usuario, entry_contrasena, label_estado)
        )
        btn_registro.grid(row=4, column=1, padx=5, pady=5)

        # Guardar referencias según jugador
        if titulo == "Jugador 1":
            self.entry_u1 = entry_usuario
            self.entry_p1 = entry_contrasena
            self.label_estado1 = label_estado
        else:
            self.entry_u2 = entry_usuario
            self.entry_p2 = entry_contrasena
            self.label_estado2 = label_estado

        return frame

    def _login(self, jugador, entry_u, entry_p, label):
        """Intenta iniciar sesión con las credenciales ingresadas."""
        usuario = entry_u.get().strip()
        contrasena = entry_p.get().strip()

        if not usuario or not contrasena:
            label.config(text="⚠ Completa todos los campos", fg="#ffaa00")
            return

        datos = iniciar_sesion(usuario, contrasena)
        if datos:
            # Verificar que no sea el mismo jugador
            if jugador == "Jugador 2" and self.jugador1 and self.jugador1["usuario"] == usuario:
                label.config(text="⚠ Este jugador ya inició sesión", fg="#ffaa00")
                return

            label.config(text=f"✅ Bienvenido, {usuario}!", fg="#00ff88")
            if jugador == "Jugador 1":
                self.jugador1 = datos
            else:
                self.jugador2 = datos
        else:
            label.config(text="❌ Usuario o contraseña incorrectos", fg="#ff4444")

    def _registro(self, entry_u, entry_p, label):
        """Registra un nuevo jugador."""
        usuario = entry_u.get().strip()
        contrasena = entry_p.get().strip()

        if not usuario or not contrasena:
            label.config(text="⚠ Completa todos los campos", fg="#ffaa00")
            return

        if len(contrasena) < 4:
            label.config(text="⚠ Contraseña mínimo 4 caracteres", fg="#ffaa00")
            return

        exito = registrar_jugador(usuario, contrasena)
        if exito:
            label.config(text=f"✅ Registrado! Ahora inicia sesión", fg="#00ff88")
        else:
            label.config(text="❌ El usuario ya existe", fg="#ff4444")

    def iniciar_partida(self):
        """Verifica que ambos jugadores hayan iniciado sesión."""
        if not self.jugador1:
            messagebox.showwarning("Falta", "El Jugador 1 debe iniciar sesión")
            return
        if not self.jugador2:
            messagebox.showwarning("Falta", "El Jugador 2 debe iniciar sesión")
            return

        self.callback_inicio(self.jugador1, self.jugador2)

    def ver_ranking(self):
        """Abre la ventana de ranking."""
        from ventanas.ranking import VentanaRanking
        VentanaRanking(self.root)
