# ============================================================
# login.py - Ventana de Login y Registro (Rediseño moderno)
# ============================================================

import tkinter as tk
from tkinter import messagebox
from clases.archivo_jugadores import registrar_jugador, iniciar_sesion

class VentanaLogin:
    def __init__(self, root, callback_inicio):
        self.root = root
        self.callback_inicio = callback_inicio
        self.jugador1 = None
        self.jugador2 = None

        self.root.title("Defensa y Asalto de Base")
        self.root.geometry("600x720")
        self.root.configure(bg="#0d0d1a")
        self.root.resizable(False, False)

        self.construir_ui()

    def construir_ui(self):
        # ── Banner superior ──
        banner = tk.Frame(self.root, bg="#e94560", height=6)
        banner.pack(fill="x")

        # ── Título ──
        frame_titulo = tk.Frame(self.root, bg="#0d0d1a")
        frame_titulo.pack(pady=(25, 5))

        tk.Label(frame_titulo, text="⚔️", font=("Arial", 32),
                 bg="#0d0d1a", fg="#e94560").pack()
        tk.Label(frame_titulo, text="DEFENSA Y ASALTO DE BASE",
                 font=("Arial", 16, "bold"), bg="#0d0d1a", fg="white").pack()
        tk.Label(frame_titulo, text="Inicia sesión o regístrate para jugar",
                 font=("Arial", 9), bg="#0d0d1a", fg="#666688").pack(pady=(3,0))

        # ── Botón ranking arriba ──
        tk.Button(
            frame_titulo,
            text="🏆  Ver Ranking",
            font=("Arial", 9),
            bg="#0f3460", fg="#ffaa00",
            activebackground="#1a4a80",
            relief="flat", padx=12, pady=5,
            cursor="hand2",
            command=self.ver_ranking
        ).pack(pady=(10, 0))

        # ── Botón música ──
        from clases.musica import reproductor
        self.musica_activa = reproductor.activa
        self.btn_musica = tk.Button(
            frame_titulo,
            text="🎵 Música: ON" if self.musica_activa else "🔇 Música: OFF",
            font=("Arial", 9),
            bg="#1a1a2e", fg="#aaaaaa",
            activebackground="#252540",
            relief="flat", padx=12, pady=4,
            cursor="hand2",
            command=self.toggle_musica
        )
        self.btn_musica.pack(pady=(5, 0))

        # ── Cards de jugadores ──
        frame_cards = tk.Frame(self.root, bg="#0d0d1a")
        frame_cards.pack(padx=25, pady=15, fill="x")

        self._crear_card(frame_cards, "Jugador 1", "🗡️", "#e94560", 0)
        self._crear_card(frame_cards, "Jugador 2", "🛡️", "#00b4d8", 1)

        # ── Botón iniciar ──
        frame_btn = tk.Frame(self.root, bg="#0d0d1a")
        frame_btn.pack(pady=10)

        self.btn_iniciar = tk.Button(
            frame_btn,
            text="  🎮  INICIAR PARTIDA  ",
            font=("Arial", 13, "bold"),
            bg="#e94560", fg="white",
            activebackground="#c73652",
            relief="flat", padx=10, pady=12,
            cursor="hand2",
            command=self.iniciar_partida
        )
        self.btn_iniciar.pack(ipadx=20)

        # ── Banner inferior ──
        tk.Frame(self.root, bg="#e94560", height=4).pack(fill="x", side="bottom")

    def _crear_card(self, parent, titulo, icono, color_acento, idx):
        """Crea una card moderna para cada jugador."""
        # Card principal
        card = tk.Frame(parent, bg="#13132a", pady=18, padx=20,
                        highlightbackground=color_acento,
                        highlightthickness=2)
        card.pack(fill="x", pady=8)

        # Header de la card
        header = tk.Frame(card, bg="#13132a")
        header.pack(fill="x", pady=(0, 12))

        tk.Label(header, text=icono, font=("Arial", 20),
                 bg="#13132a", fg=color_acento).pack(side="left", padx=(0, 10))

        frame_titulo = tk.Frame(header, bg="#13132a")
        frame_titulo.pack(side="left")
        tk.Label(frame_titulo, text=titulo, font=("Arial", 13, "bold"),
                 bg="#13132a", fg="white").pack(anchor="w")

        # Label de estado (conectado o no)
        label_estado = tk.Label(frame_titulo, text="● No conectado",
                                font=("Arial", 8), bg="#13132a", fg="#666688")
        label_estado.pack(anchor="w")

        # Separador
        tk.Frame(card, bg=color_acento, height=1).pack(fill="x", pady=(0, 12))

        # Campos
        frame_campos = tk.Frame(card, bg="#13132a")
        frame_campos.pack(fill="x")

        # Usuario
        tk.Label(frame_campos, text="USUARIO", font=("Arial", 7, "bold"),
                 bg="#13132a", fg="#666688").grid(row=0, column=0, sticky="w", pady=(0,2))
        entry_usuario = tk.Entry(frame_campos, font=("Arial", 11), width=22,
                                  bg="#1e1e3a", fg="white", insertbackground="white",
                                  relief="flat", bd=5)
        entry_usuario.grid(row=1, column=0, padx=(0,10), pady=(0,10), ipady=4)

        # Contraseña
        tk.Label(frame_campos, text="CONTRASEÑA", font=("Arial", 7, "bold"),
                 bg="#13132a", fg="#666688").grid(row=0, column=1, sticky="w", pady=(0,2))
        entry_contrasena = tk.Entry(frame_campos, font=("Arial", 11), width=22,
                                     bg="#1e1e3a", fg="white", insertbackground="white",
                                     relief="flat", bd=5, show="•")
        entry_contrasena.grid(row=1, column=1, pady=(0,10), ipady=4)

        # Botones
        frame_botones = tk.Frame(card, bg="#13132a")
        frame_botones.pack(fill="x")

        tk.Button(
            frame_botones,
            text="Iniciar Sesión",
            font=("Arial", 9, "bold"),
            bg=color_acento, fg="white",
            activebackground=color_acento,
            relief="flat", padx=12, pady=6,
            cursor="hand2",
            command=lambda: self._login(titulo, entry_usuario, entry_contrasena, label_estado)
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            frame_botones,
            text="Registrarse",
            font=("Arial", 9),
            bg="#1e1e3a", fg="#aaaaaa",
            activebackground="#252545",
            relief="flat", padx=12, pady=6,
            cursor="hand2",
            command=lambda: self._registro(entry_usuario, entry_contrasena, label_estado)
        ).pack(side="left")

        # Guardar referencias
        if idx == 0:
            self.entry_u1 = entry_usuario
            self.entry_p1 = entry_contrasena
            self.label_estado1 = label_estado
        else:
            self.entry_u2 = entry_usuario
            self.entry_p2 = entry_contrasena
            self.label_estado2 = label_estado

    def toggle_musica(self):
        """Alterna la música on/off."""
        from clases.musica import reproductor
        activa = reproductor.toggle()
        if activa:
            self.btn_musica.config(text="🎵 Música: ON", fg="#00ff88")
        else:
            self.btn_musica.config(text="🔇 Música: OFF", fg="#aaaaaa")

    def _login(self, jugador, entry_u, entry_p, label):
        usuario = entry_u.get().strip()
        contrasena = entry_p.get().strip()

        if not usuario or not contrasena:
            label.config(text="⚠ Completa todos los campos", fg="#ffaa00")
            return

        datos = iniciar_sesion(usuario, contrasena)
        if datos:
            if jugador == "Jugador 2" and self.jugador1 and self.jugador1["usuario"] == usuario:
                label.config(text="⚠ Este jugador ya inició sesión", fg="#ffaa00")
                return

            label.config(text=f"● Conectado como {usuario}", fg="#00ff88")
            if jugador == "Jugador 1":
                self.jugador1 = datos
            else:
                self.jugador2 = datos
        else:
            label.config(text="● Usuario o contraseña incorrectos", fg="#e94560")

    def _registro(self, entry_u, entry_p, label):
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
            label.config(text="✅ Registrado! Ahora inicia sesión", fg="#00ff88")
        else:
            label.config(text="● El usuario ya existe", fg="#e94560")

    def iniciar_partida(self):
        if not self.jugador1:
            messagebox.showwarning("Falta", "El Jugador 1 debe iniciar sesión")
            return
        if not self.jugador2:
            messagebox.showwarning("Falta", "El Jugador 2 debe iniciar sesión")
            return
        self.callback_inicio(self.jugador1, self.jugador2)

    def ver_ranking(self):
        from ventanas.ranking import VentanaRanking
        VentanaRanking(self.root)