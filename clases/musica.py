# ============================================================
# musica.py - Reproductor de música con winsound
# ============================================================

import threading
import os

try:
    import winsound
    WINSOUND_DISPONIBLE = True
except ImportError:
    WINSOUND_DISPONIBLE = False

RUTA_MUSICA = "assets/sonidos/musica.wav"

class ReproductorMusica:
    def __init__(self):
        self.activa = False
        self.hilo = None

    def iniciar(self):
        if not WINSOUND_DISPONIBLE or not os.path.exists(RUTA_MUSICA):
            return
        if self.activa:
            return
        self.activa = True
        self.hilo = threading.Thread(target=self._loop, daemon=True)
        self.hilo.start()

    def _loop(self):
        while self.activa:
            try:
                winsound.PlaySound(RUTA_MUSICA, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
                # Con SND_LOOP y SND_ASYNC, winsound maneja el loop solo
                # Solo esperamos hasta que se detenga
                import time
                while self.activa:
                    time.sleep(0.5)
                break
            except Exception:
                break

    def detener(self):
        self.activa = False
        if WINSOUND_DISPONIBLE:
            try:
                winsound.PlaySound(None, winsound.SND_ASYNC)
            except Exception:
                pass

    def toggle(self):
        if self.activa:
            self.detener()
            return False
        else:
            self.iniciar()
            return True

reproductor = ReproductorMusica()