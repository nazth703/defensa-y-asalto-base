# ============================================================
# combate.py - Lógica del combate automático
# ============================================================

def ejecutar_turno(torres, muros, unidades, base, matriz, dinero_defensor, dinero_atacante):
    """
    Ejecuta un turno completo de combate.
    Retorna un diccionario con el nuevo estado del dinero.
    """
    ganancia_defensor = 0
    ganancia_atacante = 0

    # 1. Las torres atacan a las unidades en su alcance
    for torre in torres:
        if torre.esta_destruida():
            continue

        objetivo = _buscar_unidad_en_alcance(torre, unidades)
        if objetivo:
            danio = torre.atacar(objetivo)

            # El defensor gana dinero por dañar unidades
            ganancia_defensor += danio // 5

            # Habilidad especial si está lista
            if torre.habilidad_lista():
                torre.habilidad_especial(unidades, torres)

            # Si la unidad murió, el defensor gana recompensa
            if objetivo.esta_muerta():
                recompensa = {"Soldado": 15, "Tanque": 40, "Unidad Rápida": 20}
                ganancia_defensor += recompensa.get(objetivo.nombre, 10)

    # 2. Las unidades se mueven y atacan
    for unidad in unidades:
        if unidad.esta_muerta():
            continue

        # Buscar torre o muro en la casilla destino
        torre_bloqueando = _buscar_torre_adelante(unidad, torres, muros)

        if torre_bloqueando:
            # Atacar la torre/muro en lugar de moverse
            danio = unidad.atacar_torre(torre_bloqueando)
            ganancia_atacante += danio // 5

            if torre_bloqueando.esta_destruida():
                # Limpiar de la matriz
                if hasattr(torre_bloqueando, 'fila') and torre_bloqueando.fila is not None:
                    matriz[torre_bloqueando.fila][torre_bloqueando.columna] = None
                ganancia_atacante += 20  # Bonus por destruir

            # Habilidad especial si está lista
            if unidad.habilidad_lista():
                unidad.habilidad_especial(torres + muros, base)
        else:
            # Mover la unidad
            if unidad.fila is not None and unidad.columna is not None:
                matriz[unidad.fila][unidad.columna] = None

            llego_a_base = unidad.mover(matriz)

            if llego_a_base or unidad.columna <= base.columna:
                # Atacar la base
                danio = unidad.atacar_base(base)
                ganancia_atacante += danio // 3
            else:
                if unidad.fila is not None:
                    matriz[unidad.fila][unidad.columna] = unidad

    return {
        "dinero_defensor": dinero_defensor + ganancia_defensor,
        "dinero_atacante": dinero_atacante + ganancia_atacante
    }


def _buscar_unidad_en_alcance(torre, unidades):
    """Retorna la primera unidad viva dentro del alcance de la torre."""
    for unidad in unidades:
        if not unidad.esta_muerta() and torre.puede_atacar(unidad.fila, unidad.columna):
            return unidad
    return None


def _buscar_torre_adelante(unidad, torres, muros):
    """
    Busca si hay una torre o muro bloqueando el camino de la unidad.
    Revisa las casillas adelante según la velocidad.
    """
    if unidad.fila is None or unidad.columna is None:
        return None

    col_destino = max(0, unidad.columna - unidad.velocidad)

    for estructura in torres + muros:
        if estructura.esta_destruida() if hasattr(estructura, 'esta_destruida') else False:
            continue
        if estructura.fila == unidad.fila and col_destino <= estructura.columna < unidad.columna:
            return estructura
    return None