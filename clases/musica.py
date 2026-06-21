# ============================================================
# musica.py - Reproductor de música con winsound
# ============================================================

import threading
import os

# Intentar importar winsound (solo Windows)
try:
    import winsound
    WINSOUND_DISPONIBLE = True
except ImportError:
    WINSOUND_DISPONIBLE = False

RUTA_MUSICA = "assets/sonidos/musica.wav"

class ReproductorMusica:
    """
    Maneja la reproducción de música de fondo en un hilo separado.
    Usa winsound que viene incluido en Python para Windows.
    """

    def __init__(self):
        self.activa = False
        self.hilo = None

    def iniciar(self):
        """Inicia la reproducción de música en loop."""
        if not WINSOUND_DISPONIBLE:
            return
        if not os.path.exists(RUTA_MUSICA):
            return
        if self.activa:
            return

        self.activa = True
        self.hilo = threading.Thread(target=self._loop, daemon=True)
        self.hilo.start()

    def _loop(self):
        """Reproduce el archivo WAV en loop mientras activa sea True."""
        while self.activa:
            try:
                winsound.PlaySound(RUTA_MUSICA, winsound.SND_FILENAME)
            except Exception:
                break

    def detener(self):
        """Detiene la música."""
        self.activa = False
        if WINSOUND_DISPONIBLE:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except Exception:
                pass

    def toggle(self):
        """Alterna entre reproducir y detener."""
        if self.activa:
            self.detener()
            return False
        else:
            self.iniciar()
            return True

    def disponible(self):
        """Retorna True si winsound está disponible y el archivo existe."""
        return WINSOUND_DISPONIBLE and os.path.exists(RUTA_MUSICA)


# Instancia global del reproductor
reproductor = ReproductorMusica()