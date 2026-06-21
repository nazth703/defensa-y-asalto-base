# ============================================================
# mapa.py - Ventana principal del juego con cuadrícula 10x10
# ============================================================

import tkinter as tk
from tkinter import messagebox
from clases.torre import TorreBasica, TorrePesada, TorreMagica
from clases.unidad import Soldado, Tanque, UnidadRapida
from clases.estructuras import BaseCentral, Muro

# Tamaño de cada casilla en píxeles
TAMANIO_CASILLA = 55
FILAS = 10
COLUMNAS = 10

# Colores del mapa
COLOR_VACIO      = "#2d2d44"
COLOR_BASE       = "#e94560"
COLOR_MURO       = "#8B4513"
COLOR_TORRE      = "#0f3460"
COLOR_UNIDAD     = "#e67e22"
COLOR_HOVER      = "#3d3d5c"
COLOR_BORDE      = "#1a1a2e"

class VentanaMapa:
    """
    Ventana principal del juego.
    Muestra la cuadrícula y maneja las fases de construcción y ataque.
    """

    def __init__(self, root, jugador1, faccion1, jugador2, faccion2):
        self.root = root
        self.jugador1 = jugador1   # Diccionario con datos
        self.jugador2 = jugador2
        self.faccion1 = faccion1   # Defensor
        self.faccion2 = faccion2   # Atacante

        # Estado del juego
        self.ronda_actual = 1
        self.rondas_ganadas_j1 = 0  # Defensor
        self.rondas_ganadas_j2 = 0  # Atacante
        self.fase = "construccion"   # "construccion" o "ataque"
        self.elemento_seleccionado = None  # Qué quiere colocar el jugador

        # Dinero inicial
        self.dinero_defensor = 200
        self.dinero_atacante = 200
        self.pausado = False

        # Estructuras en el mapa
        self.matriz = [[None] * COLUMNAS for _ in range(FILAS)]
        self.base = BaseCentral(faccion1)
        self.torres = []
        self.muros = []
        self.unidades = []

        # Base central fija en columna 0, fila 4 (centro izquierda)
        self.base.fila = 4
        self.base.columna = 0
        self.matriz[4][0] = self.base

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Defensa y Asalto de Base")
        self.ventana.configure(bg="#1a1a2e")
        self.ventana.resizable(False, False)

        self.construir_ui()
        self.dibujar_mapa()
        self.actualizar_info()

    def construir_ui(self):
        """Construye toda la interfaz."""

        # ── Panel superior: info de ronda ──
        self.frame_info = tk.Frame(self.ventana, bg="#16213e", pady=8)
        self.frame_info.pack(fill="x", padx=10, pady=(10, 0))

        self.label_ronda = tk.Label(
            self.frame_info, text="", font=("Arial", 13, "bold"),
            bg="#16213e", fg="#e94560"
        )
        self.label_ronda.pack(side="left", padx=15)

        self.label_fase = tk.Label(
            self.frame_info, text="", font=("Arial", 11),
            bg="#16213e", fg="#00ff88"
        )
        self.label_fase.pack(side="left", padx=15)

        self.label_marcador = tk.Label(
            self.frame_info, text="", font=("Arial", 11),
            bg="#16213e", fg="#ffaa00"
        )
        self.label_marcador.pack(side="right", padx=15)

        # Botón de pausa
        tk.Button(
            self.frame_info,
            text="⏸ Pausa",
            font=("Arial", 9, "bold"),
            bg="#333355", fg="white",
            activebackground="#444466",
            relief="flat", padx=10, pady=4,
            cursor="hand2",
            command=self.abrir_pausa
        ).pack(side="right", padx=5)

        # ── Frame central: mapa + panel lateral ──
        frame_central = tk.Frame(self.ventana, bg="#1a1a2e")
        frame_central.pack(padx=10, pady=10)

        # Canvas del mapa
        ancho = COLUMNAS * TAMANIO_CASILLA
        alto  = FILAS * TAMANIO_CASILLA
        self.canvas = tk.Canvas(
            frame_central, width=ancho, height=alto,
            bg=COLOR_VACIO, highlightthickness=0
        )
        self.canvas.pack(side="left", padx=(0, 10))
        self.canvas.bind("<Button-1>", self.click_casilla)
        self.canvas.bind("<Button-3>", self.click_derecho_casilla)
        self.canvas.bind("<Motion>", self.hover_casilla)

        # Panel lateral
        self.frame_lateral = tk.Frame(frame_central, bg="#16213e", width=220, pady=10)
        self.frame_lateral.pack(side="left", fill="y")
        self.frame_lateral.pack_propagate(False)

        self.construir_panel_lateral()

    def abrir_pausa(self):
        """Abre el menú de pausa."""
        self.pausado = True

        pausa = tk.Toplevel(self.ventana)
        pausa.title("Pausa")
        pausa.geometry("300x320")
        pausa.configure(bg="#0d0d1a")
        pausa.resizable(False, False)
        pausa.grab_set()

        # Título
        tk.Frame(pausa, bg="#e94560", height=4).pack(fill="x")

        tk.Label(pausa, text="⏸", font=("Arial", 30),
                 bg="#0d0d1a", fg="#e94560").pack(pady=(20, 5))
        tk.Label(pausa, text="JUEGO EN PAUSA",
                 font=("Arial", 14, "bold"),
                 bg="#0d0d1a", fg="white").pack()
        tk.Label(pausa, text=f"Ronda {self.ronda_actual}",
                 font=("Arial", 9), bg="#0d0d1a", fg="#666688").pack(pady=(2, 20))

        # Botones
        def reanudar():
            self.pausado = False
            pausa.destroy()

        def reiniciar():
            if messagebox.askyesno("Reiniciar", "¿Seguro que quieres reiniciar la partida?",
                                    parent=pausa):
                pausa.destroy()
                self.ventana.destroy()
                from ventanas.mapa import VentanaMapa
                VentanaMapa(self.root, self.jugador1, self.faccion1,
                            self.jugador2, self.faccion2)

        def menu_principal():
            if messagebox.askyesno("Menú Principal", "¿Salir al menú principal? Se perderá el progreso.",
                                    parent=pausa):
                pausa.destroy()
                self.ventana.destroy()

        estilo_btn = {
            "font": ("Arial", 11, "bold"),
            "relief": "flat",
            "padx": 20, "pady": 10,
            "cursor": "hand2",
            "width": 20
        }

        tk.Button(pausa, text="▶  Reanudar",
                  bg="#00b44d", fg="white",
                  activebackground="#009940",
                  command=reanudar, **estilo_btn).pack(pady=5)

        tk.Button(pausa, text="🔄  Reiniciar Partida",
                  bg="#0f3460", fg="white",
                  activebackground="#1a4a80",
                  command=reiniciar, **estilo_btn).pack(pady=5)

        tk.Button(pausa, text="🏠  Menú Principal",
                  bg="#333355", fg="#aaaaaa",
                  activebackground="#444466",
                  command=menu_principal, **estilo_btn).pack(pady=5)

        # Botón música
        from clases.musica import reproductor
        def toggle_musica_pausa():
            activa = reproductor.toggle()
            btn_musica_pausa.config(
                text="🎵 Música: ON" if activa else "🔇 Música: OFF",
                fg="#00ff88" if activa else "#aaaaaa"
            )

        btn_musica_pausa = tk.Button(
            pausa,
            text="🎵 Música: ON" if reproductor.activa else "🔇 Música: OFF",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#00ff88" if reproductor.activa else "#aaaaaa",
            activebackground="#252540",
            relief="flat", padx=20, pady=6,
            cursor="hand2",
            command=toggle_musica_pausa
        )
        btn_musica_pausa.pack(pady=(10, 5))

        tk.Frame(pausa, bg="#e94560", height=4).pack(fill="x", side="bottom")

    def construir_panel_lateral(self):
        """Panel con opciones de compra según la fase."""
        for widget in self.frame_lateral.winfo_children():
            widget.destroy()

        if self.fase == "construccion":
            self._panel_defensor()
        else:
            self._panel_atacante()

    def _panel_defensor(self):
        """Panel de compra para el defensor."""
        tk.Label(
            self.frame_lateral,
            text=f"🏰 {self.jugador1['usuario']}",
            font=("Arial", 12, "bold"),
            bg="#16213e", fg="#00ff88"
        ).pack(pady=(5, 2))

        self.label_dinero_def = tk.Label(
            self.frame_lateral,
            text=f"💰 ${self.dinero_defensor}",
            font=("Arial", 11),
            bg="#16213e", fg="#ffaa00"
        )
        self.label_dinero_def.pack(pady=(0, 10))

        tk.Label(self.frame_lateral, text="── Comprar ──",
                 bg="#16213e", fg="#aaaaaa", font=("Arial", 9)).pack()

        items = [
            ("🧱 Muro ($20)",         "muro",         20),
            ("🗼 Torre Básica ($50)",  "torre_basica",  50),
            ("⚔️ Torre Pesada ($120)", "torre_pesada", 120),
            ("✨ Torre Mágica ($80)",  "torre_magica",  80),
        ]

        for texto, clave, costo in items:
            btn = tk.Button(
                self.frame_lateral,
                text=texto,
                font=("Arial", 9),
                bg="#0f3460", fg="white",
                relief="flat", pady=5,
                command=lambda c=clave: self.seleccionar_elemento(c)
            )
            btn.pack(fill="x", padx=10, pady=3)

        tk.Label(self.frame_lateral, text="",bg="#16213e").pack(pady=5)

        tk.Button(
            self.frame_lateral,
            text="▶ Terminar Construcción",
            font=("Arial", 9, "bold"),
            bg="#e94560", fg="white",
            relief="flat", pady=7,
            command=self.terminar_construccion
        ).pack(fill="x", padx=10, pady=5)

        self.label_seleccion = tk.Label(
            self.frame_lateral, text="Selecciona un elemento\ny haz click en el mapa",
            bg="#16213e", fg="#aaaaaa", font=("Arial", 8), wraplength=180
        )
        self.label_seleccion.pack(pady=10)

    def _panel_atacante(self):
        """Panel de compra para el atacante."""
        tk.Label(
            self.frame_lateral,
            text=f"⚔️ {self.jugador2['usuario']}",
            font=("Arial", 12, "bold"),
            bg="#16213e", fg="#e94560"
        ).pack(pady=(5, 2))

        self.label_dinero_atk = tk.Label(
            self.frame_lateral,
            text=f"💰 ${self.dinero_atacante}",
            font=("Arial", 11),
            bg="#16213e", fg="#ffaa00"
        )
        self.label_dinero_atk.pack(pady=(0, 10))

        tk.Label(self.frame_lateral, text="── Comprar ──",
                 bg="#16213e", fg="#aaaaaa", font=("Arial", 9)).pack()

        items = [
            ("🗡️ Soldado ($30)",      "soldado", 30),
            ("🛡️ Tanque ($100)",      "tanque",  100),
            ("💨 Unidad Rápida ($50)", "rapida",  50),
        ]

        for texto, clave, costo in items:
            btn = tk.Button(
                self.frame_lateral,
                text=texto,
                font=("Arial", 9),
                bg="#533483", fg="white",
                relief="flat", pady=5,
                command=lambda c=clave: self.seleccionar_elemento(c)
            )
            btn.pack(fill="x", padx=10, pady=3)

        tk.Label(self.frame_lateral, text="", bg="#16213e").pack(pady=5)

        tk.Button(
            self.frame_lateral,
            text="▶ Iniciar Combate",
            font=("Arial", 9, "bold"),
            bg="#e94560", fg="white",
            relief="flat", pady=7,
            command=self.iniciar_combate
        ).pack(fill="x", padx=10, pady=5)

        self.label_seleccion = tk.Label(
            self.frame_lateral, text="Selecciona una unidad\ny haz click en el mapa",
            bg="#16213e", fg="#aaaaaa", font=("Arial", 8), wraplength=180
        )
        self.label_seleccion.pack(pady=10)

    def seleccionar_elemento(self, clave):
        """Guarda qué elemento quiere colocar el jugador."""
        self.elemento_seleccionado = clave
        nombres = {
            "muro": "Muro", "torre_basica": "Torre Básica",
            "torre_pesada": "Torre Pesada", "torre_magica": "Torre Mágica",
            "soldado": "Soldado", "tanque": "Tanque", "rapida": "Unidad Rápida"
        }
        self.label_seleccion.config(
            text=f"Seleccionado:\n{nombres.get(clave, clave)}\nHaz click en el mapa",
            fg="#00ff88"
        )

    def click_casilla(self, event):
        """Maneja el click izquierdo en el mapa para colocar elementos."""
        col = event.x // TAMANIO_CASILLA
        fila = event.y // TAMANIO_CASILLA

        if not (0 <= fila < FILAS and 0 <= col < COLUMNAS):
            return
        if self.elemento_seleccionado is None:
            return
        if self.matriz[fila][col] is not None:
            return  # Casilla ocupada

        if self.fase == "construccion":
            self._colocar_defensa(fila, col)
        else:
            self._colocar_unidad(fila, col)

    def click_derecho_casilla(self, event):
        """Click derecho: retira el elemento y devuelve el dinero completo."""
        col = event.x // TAMANIO_CASILLA
        fila = event.y // TAMANIO_CASILLA

        if not (0 <= fila < FILAS and 0 <= col < COLUMNAS):
            return
        if self.fase == "combate":
            return  # No se puede retirar durante el combate

        elemento = self.matriz[fila][col]
        if elemento is None or elemento == self.base:
            return  # No hay nada que retirar o es la base

        costos = {
            "Muro": 20, "Torre Básica": 50,
            "Torre Pesada": 120, "Torre Mágica": 80,
            "Soldado": 30, "Tanque": 100, "Unidad Rápida": 50
        }
        nombre = elemento.nombre if hasattr(elemento, 'nombre') else ""
        reembolso = costos.get(nombre, 0)

        # Retirar del mapa y listas
        self.matriz[fila][col] = None
        self.torres  = [t for t in self.torres  if not (t.fila == fila and t.columna == col)]
        self.muros   = [m for m in self.muros   if not (m.fila == fila and m.columna == col)]
        self.unidades = [u for u in self.unidades if not (u.fila == fila and u.columna == col)]

        # Devolver dinero
        if self.fase == "construccion":
            self.dinero_defensor += reembolso
            if hasattr(self, 'label_dinero_def'):
                self.label_dinero_def.config(text=f"💰 ${self.dinero_defensor}")
        else:
            self.dinero_atacante += reembolso
            if hasattr(self, 'label_dinero_atk'):
                self.label_dinero_atk.config(text=f"💰 ${self.dinero_atacante}")

        self.dibujar_mapa()
        if hasattr(self, 'label_seleccion'):
            self.label_seleccion.config(
                text=f"✅ Retirado!\n+${reembolso} devuelto",
                fg="#ffaa00"
            )

    def _colocar_defensa(self, fila, col):
        """Coloca una torre o muro en el mapa."""
        costos = {
            "muro": 20, "torre_basica": 50,
            "torre_pesada": 120, "torre_magica": 80
        }
        costo = costos.get(self.elemento_seleccionado, 0)

        if self.dinero_defensor < costo:
            messagebox.showwarning("Sin dinero", f"No tienes suficiente dinero (${costo})")
            return

        faccion = self.faccion1
        elemento = None

        if self.elemento_seleccionado == "muro":
            elemento = Muro(faccion)
        elif self.elemento_seleccionado == "torre_basica":
            elemento = TorreBasica(faccion)
        elif self.elemento_seleccionado == "torre_pesada":
            elemento = TorrePesada(faccion)
        elif self.elemento_seleccionado == "torre_magica":
            elemento = TorreMagica(faccion)

        if elemento:
            elemento.fila = fila
            elemento.columna = col
            self.matriz[fila][col] = elemento
            self.dinero_defensor -= costo

            if self.elemento_seleccionado == "muro":
                self.muros.append(elemento)
            else:
                self.torres.append(elemento)

            self.dibujar_mapa()
            self.label_dinero_def.config(text=f"💰 ${self.dinero_defensor}")

    def _colocar_unidad(self, fila, col):
        """Coloca una unidad atacante en el mapa (solo columnas derechas)."""
        if col < COLUMNAS - 3:
            messagebox.showwarning("Posición inválida", "Las unidades deben colocarse en las 3 columnas de la derecha")
            return

        costos = {"soldado": 30, "tanque": 100, "rapida": 50}
        costo = costos.get(self.elemento_seleccionado, 0)

        if self.dinero_atacante < costo:
            messagebox.showwarning("Sin dinero", f"No tienes suficiente dinero (${costo})")
            return

        faccion = self.faccion2
        unidad = None

        if self.elemento_seleccionado == "soldado":
            unidad = Soldado(faccion)
        elif self.elemento_seleccionado == "tanque":
            unidad = Tanque(faccion)
        elif self.elemento_seleccionado == "rapida":
            unidad = UnidadRapida(faccion)

        if unidad:
            unidad.fila = fila
            unidad.columna = col
            self.matriz[fila][col] = unidad
            self.dinero_atacante -= costo
            self.unidades.append(unidad)

            self.dibujar_mapa()
            self.label_dinero_atk.config(text=f"💰 ${self.dinero_atacante}")

    def hover_casilla(self, event):
        """Resalta la casilla bajo el cursor."""
        self.dibujar_mapa()
        col = event.x // TAMANIO_CASILLA
        fila = event.y // TAMANIO_CASILLA
        if 0 <= fila < FILAS and 0 <= col < COLUMNAS:
            x1 = col * TAMANIO_CASILLA
            y1 = fila * TAMANIO_CASILLA
            x2 = x1 + TAMANIO_CASILLA
            y2 = y1 + TAMANIO_CASILLA
            if self.matriz[fila][col] is None:
                self.canvas.create_rectangle(x1, y1, x2, y2,
                    fill=COLOR_HOVER, outline=COLOR_BORDE)

    def dibujar_mapa(self):
        """Redibuja todo el mapa."""
        self.canvas.delete("all")

        # Dibujar línea divisoria entre zona defensa y ataque
        x_div = 5 * TAMANIO_CASILLA
        self.canvas.create_line(
            x_div, 0, x_div, FILAS * TAMANIO_CASILLA,
            fill="#e94560", width=2, dash=(6, 3)
        )

        # Etiquetas de zona
        self.canvas.create_text(
            2 * TAMANIO_CASILLA, 8,
            text=f"🏰 Zona {self.faccion1}",
            font=("Arial", 7, "bold"), fill="#aaaaaa"
        )
        self.canvas.create_text(
            7 * TAMANIO_CASILLA, 8,
            text=f"⚔️ Zona {self.faccion2}",
            font=("Arial", 7, "bold"), fill="#aaaaaa"
        )

        # Colores de zona según facción
        zonas_defensa = {
            "Medieval":   "#1e1200",
            "Naturaleza": "#0a1a0a",
            "Oscura":     "#0f0010",
        }
        zonas_ataque = {
            "Medieval":   "#1a0a00",
            "Naturaleza": "#001a0a",
            "Oscura":     "#100010",
        }
        colores_torre = {
            "Medieval":   "#5c3317",
            "Naturaleza": "#1a5c17",
            "Oscura":     "#3d0a5c",
        }
        colores_muro = {
            "Medieval":   "#8B4513",
            "Naturaleza": "#2d6e1a",
            "Oscura":     "#4a0a6e",
        }

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1 = col * TAMANIO_CASILLA
                y1 = fila * TAMANIO_CASILLA
                x2 = x1 + TAMANIO_CASILLA
                y2 = y1 + TAMANIO_CASILLA

                elemento = self.matriz[fila][col]
                es_base = (fila == self.base.fila and col == self.base.columna)

                # Color de fondo por zona
                if col <= 4:
                    color_fondo = zonas_defensa.get(self.faccion1, COLOR_VACIO)
                else:
                    color_fondo = zonas_ataque.get(self.faccion2, COLOR_VACIO)

                if es_base:
                    color = COLOR_BASE
                    texto = "🏰"
                elif elemento is None:
                    color = color_fondo
                    texto = ""
                elif "Muro" in type(elemento).__name__:
                    color = colores_muro.get(self.faccion1, COLOR_MURO)
                    texto = "🧱"
                elif type(elemento).__name__ == "TorreBasica":
                    color = colores_torre.get(self.faccion1, COLOR_TORRE)
                    texto = "🗼"
                elif type(elemento).__name__ == "TorrePesada":
                    color = colores_torre.get(self.faccion1, "#1a4a1a")
                    texto = "🏯"
                elif type(elemento).__name__ == "TorreMagica":
                    color = colores_torre.get(self.faccion1, "#2d0a4e")
                    texto = "🔮"
                elif type(elemento).__name__ == "Soldado":
                    color = COLOR_UNIDAD
                    texto = "🗡️"
                elif type(elemento).__name__ == "Tanque":
                    color = "#7a3500"
                    texto = "🛡️"
                elif type(elemento).__name__ == "UnidadRapida":
                    color = "#5a2080"
                    texto = "💨"
                else:
                    color = COLOR_UNIDAD
                    texto = "⚔️"

                self.canvas.create_rectangle(x1, y1, x2, y2,
                    fill=color, outline=COLOR_BORDE, width=1)

                if texto:
                    self.canvas.create_text(
                        x1 + TAMANIO_CASILLA // 2,
                        y1 + TAMANIO_CASILLA // 2,
                        text=texto, font=("Arial", 18)
                    )

                # Mostrar barra de vida y stats en torres, muros y unidades
                if elemento is not None and not es_base:
                    if hasattr(elemento, 'vida') and hasattr(elemento, 'vida_maxima'):
                        # Barra de vida
                        barra_ancho = TAMANIO_CASILLA - 6
                        porcentaje = elemento.vida / elemento.vida_maxima
                        color_barra = "#00ff88" if porcentaje > 0.5 else "#ffaa00" if porcentaje > 0.25 else "#ff4444"
                        # Fondo de la barra
                        self.canvas.create_rectangle(
                            x1 + 3, y2 - 7, x1 + 3 + barra_ancho, y2 - 3,
                            fill="#333333", outline=""
                        )
                        # Barra de vida actual
                        self.canvas.create_rectangle(
                            x1 + 3, y2 - 7, x1 + 3 + int(barra_ancho * porcentaje), y2 - 3,
                            fill=color_barra, outline=""
                        )
                        # Número de vida
                        self.canvas.create_text(
                            x1 + TAMANIO_CASILLA // 2, y1 + 7,
                            text=f"{elemento.vida}", font=("Arial", 7, "bold"),
                            fill="white"
                        )
                    # Mostrar daño de torres y unidades
                    if hasattr(elemento, 'danio'):
                        self.canvas.create_text(
                            x1 + TAMANIO_CASILLA - 5, y1 + 7,
                            text=f"⚡{elemento.danio}", font=("Arial", 6, "bold"),
                            fill="#ffdd00", anchor="e"
                        )

                # Mostrar vida de la base encima
                if es_base:
                    self.canvas.create_text(
                        x1 + TAMANIO_CASILLA // 2,
                        y1 + TAMANIO_CASILLA - 8,
                        text=f"{self.base.vida}", font=("Arial", 7, "bold"),
                        fill="white"
                    )
                    # Si hay unidades atacando la base, mostrar indicador
                    unidades_en_base = [u for u in self.unidades
                                       if u.fila == self.base.fila and u.columna <= self.base.columna and not u.esta_muerta()]
                    if unidades_en_base:
                        self.canvas.create_text(
                            x1 + TAMANIO_CASILLA - 8,
                            y1 + 8,
                            text="⚔️", font=("Arial", 10)
                        )

    def actualizar_info(self):
        """Actualiza los labels de información."""
        self.label_ronda.config(text=f"Ronda {self.ronda_actual}")
        fase_texto = "🏰 Fase: Construcción" if self.fase == "construccion" else "⚔️ Fase: Ataque"
        self.label_fase.config(text=fase_texto)
        self.label_marcador.config(
            text=f"{self.jugador1['usuario']}: {self.rondas_ganadas_j1} | {self.jugador2['usuario']}: {self.rondas_ganadas_j2}"
        )

    def terminar_construccion(self):
        """Pasa a la fase de ataque."""
        self.fase = "ataque"
        self.elemento_seleccionado = None
        self.construir_panel_lateral()
        self.actualizar_info()
        messagebox.showinfo("Fase de Ataque", f"¡Turno del atacante!\n{self.jugador2['usuario']} coloca sus unidades.")

    def iniciar_combate(self):
        """Inicia la fase de combate automático."""
        if not self.unidades:
            messagebox.showwarning("Sin unidades", "El atacante debe colocar al menos una unidad.")
            return
        self.fase = "combate"
        self.actualizar_info()

        # Mostrar vida de la base en el panel lateral
        for widget in self.frame_lateral.winfo_children():
            widget.destroy()
        tk.Label(self.frame_lateral, text="⚔️ COMBATE ⚔️",
                 font=("Arial", 13, "bold"), bg="#16213e", fg="#e94560").pack(pady=10)
        tk.Label(self.frame_lateral, text="🏰 Vida de la Base:",
                 font=("Arial", 10), bg="#16213e", fg="#aaaaaa").pack()
        self.label_vida_base = tk.Label(
            self.frame_lateral,
            text=f"{self.base.vida} / {self.base.vida_maxima}",
            font=("Arial", 14, "bold"), bg="#16213e", fg="#00ff88"
        )
        self.label_vida_base.pack(pady=5)

        self.ventana.after(500, self.turno_combate)

    def mostrar_danio_flotante(self, fila, col, cantidad, color="#ff4444"):
        """Muestra un número de daño flotante en el canvas que desaparece."""
        x = col * TAMANIO_CASILLA + TAMANIO_CASILLA // 2
        y = fila * TAMANIO_CASILLA + TAMANIO_CASILLA // 2
        texto_id = self.canvas.create_text(
            x, y, text=f"-{cantidad}",
            font=("Arial", 11, "bold"), fill=color
        )
        self.ventana.after(600, lambda: self.canvas.delete(texto_id))

    def turno_combate(self):
        """Ejecuta un turno de combate y programa el siguiente."""
        if self.pausado:
            self.ventana.after(200, self.turno_combate)
            return
        from clases.combate import ejecutar_turno
        resultado = ejecutar_turno(
            self.torres, self.muros, self.unidades,
            self.base, self.matriz,
            self.dinero_defensor, self.dinero_atacante
        )

        self.dinero_defensor = resultado["dinero_defensor"]
        self.dinero_atacante = resultado["dinero_atacante"]

        # Mostrar daño flotante en torres que atacaron
        for torre in self.torres:
            if torre.fila is not None and torre.contador_turnos > 0:
                for u in self.unidades:
                    if not u.esta_muerta() and torre.puede_atacar(u.fila, u.columna):
                        self.mostrar_danio_flotante(u.fila, u.columna, torre.danio, "#ff4444")
                        break

        # Mostrar daño flotante en la base si fue atacada
        for u in self.unidades:
            if not u.esta_muerta() and u.columna <= self.base.columna:
                self.mostrar_danio_flotante(self.base.fila, self.base.columna, u.danio, "#ff8800")

        # Limpiar muertos
        self.unidades = [u for u in self.unidades if not u.esta_muerta()]
        self.torres   = [t for t in self.torres   if not t.esta_destruida()]
        self.muros    = [m for m in self.muros     if not m.esta_destruido()]

        # Actualizar matriz
        self._sincronizar_matriz()
        self.dibujar_mapa()

        # Actualizar label de vida de la base
        if hasattr(self, 'label_vida_base'):
            color = '#00ff88' if self.base.vida > 250 else '#ffaa00' if self.base.vida > 100 else '#ff4444'
            self.label_vida_base.config(
                text=f'{self.base.vida} / {self.base.vida_maxima}',
                fg=color
            )

        # Verificar fin de ronda
        if self.base.esta_destruida():
            self._fin_ronda("atacante")
        elif not self.unidades:
            self._fin_ronda("defensor")
        else:
            self.ventana.after(600, self.turno_combate)

    def _sincronizar_matriz(self):
        """Actualiza la matriz con el estado actual de los elementos."""
        self.matriz = [[None] * COLUMNAS for _ in range(FILAS)]
        self.matriz[self.base.fila][self.base.columna] = self.base
        # Unidades en la base siguen en el mapa (atacando)
        for t in self.torres:
            if t.fila is not None:
                self.matriz[t.fila][t.columna] = t
        for m in self.muros:
            if m.fila is not None:
                self.matriz[m.fila][m.columna] = m
        for u in self.unidades:
            if u.fila is not None and not u.esta_muerta():
                self.matriz[u.fila][u.columna] = u

    def _fin_ronda(self, ganador):
        """Maneja el fin de una ronda."""
        if ganador == "defensor":
            self.rondas_ganadas_j1 += 1
            msg = f"🏰 ¡{self.jugador1['usuario']} ganó la ronda!"
        else:
            self.rondas_ganadas_j2 += 1
            msg = f"⚔️ ¡{self.jugador2['usuario']} ganó la ronda!"

        messagebox.showinfo("Fin de Ronda", msg)

        # Verificar ganador de partida
        if self.rondas_ganadas_j1 >= 3:
            self._fin_partida(self.jugador1, "defensor")
        elif self.rondas_ganadas_j2 >= 3:
            self._fin_partida(self.jugador2, "atacante")
        else:
            self.ronda_actual += 1
            self._nueva_ronda()

    def _nueva_ronda(self):
        """Reinicia el estado para una nueva ronda."""
        self.fase = "construccion"
        self.elemento_seleccionado = None
        self.torres = []
        self.muros = []
        self.unidades = []
        self.base.reparar()
        self.dinero_defensor += 150
        self.dinero_atacante += 150
        self.matriz = [[None] * COLUMNAS for _ in range(FILAS)]
        self.matriz[self.base.fila][self.base.columna] = self.base
        self.construir_panel_lateral()
        self.dibujar_mapa()
        self.actualizar_info()
        messagebox.showinfo("Nueva Ronda", f"¡Inicia la Ronda {self.ronda_actual}!")

    def _fin_partida(self, ganador, rol):
        """Maneja el fin de la partida completa."""
        from clases.archivo_jugadores import actualizar_victorias
        actualizar_victorias(ganador["usuario"], rol)
        messagebox.showinfo(
            "🏆 Fin de Partida",
            f"¡{ganador['usuario']} ganó la partida como {rol}!\n\n¡Felicidades!"
        )
        self.ventana.destroy()