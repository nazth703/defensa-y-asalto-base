# ============================================================
# archivo_jugadores.py - Manejo de jugadores en JSON
# ============================================================

import json
import os

RUTA_ARCHIVO = "datos/jugadores.json"

def inicializar_archivo():
    """
    Crea el archivo jugadores.json si no existe.
    Se llama al iniciar el programa.
    """
    os.makedirs("datos", exist_ok=True)
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "w") as f:
            json.dump([], f)

def cargar_jugadores():
    """
    Lee el archivo JSON y retorna una lista de diccionarios.
    """
    inicializar_archivo()
    with open(RUTA_ARCHIVO, "r") as f:
        return json.load(f)

def guardar_jugadores(lista):
    """
    Guarda la lista completa de jugadores en el JSON.
    """
    with open(RUTA_ARCHIVO, "w") as f:
        json.dump(lista, f, indent=4)

def registrar_jugador(usuario, contrasena):
    """
    Registra un nuevo jugador.
    Retorna True si se registró, False si el usuario ya existe.
    """
    jugadores = cargar_jugadores()

    # Verificar si el usuario ya existe
    for j in jugadores:
        if j["usuario"] == usuario:
            return False  # Ya existe

    nuevo = {
        "usuario": usuario,
        "contrasena": contrasena,
        "victorias_defensor": 0,
        "victorias_atacante": 0
    }
    jugadores.append(nuevo)
    guardar_jugadores(jugadores)
    return True

def iniciar_sesion(usuario, contrasena):
    """
    Verifica las credenciales del jugador.
    Retorna el diccionario del jugador si es correcto, None si no.
    """
    jugadores = cargar_jugadores()
    for j in jugadores:
        if j["usuario"] == usuario and j["contrasena"] == contrasena:
            return j
    return None

def actualizar_victorias(usuario, rol):
    """
    Suma una victoria al jugador según su rol ('defensor' o 'atacante').
    """
    jugadores = cargar_jugadores()
    for j in jugadores:
        if j["usuario"] == usuario:
            if rol == "defensor":
                j["victorias_defensor"] += 1
            elif rol == "atacante":
                j["victorias_atacante"] += 1
            break
    guardar_jugadores(jugadores)

def obtener_top_defensores(limite=5):
    """
    Retorna los top jugadores con más victorias como defensor.
    """
    jugadores = cargar_jugadores()
    ordenados = sorted(jugadores, key=lambda j: j["victorias_defensor"], reverse=True)
    return ordenados[:limite]

def obtener_top_atacantes(limite=5):
    """
    Retorna los top jugadores con más victorias como atacante.
    """
    jugadores = cargar_jugadores()
    ordenados = sorted(jugadores, key=lambda j: j["victorias_atacante"], reverse=True)
    return ordenados[:limite]

def usuario_existe(usuario):
    """Verifica si un usuario ya está registrado."""
    jugadores = cargar_jugadores()
    return any(j["usuario"] == usuario for j in jugadores)
