# Defensa y Asalto de Base

Juego de estrategia por turnos para dos jugadores desarrollado en Python con Tkinter.

**Estudiante:** Nazareth Ulate Díaz  
**Curso:** Introducción a la Programación (Modalidad Live Learning)  
**Carrera:** Ingeniería en Computación

---

## Descripción

Juego de estrategia para dos jugadores donde uno asume el rol de defensor (construye torres y muros para proteger su base) y el otro de atacante (envía unidades para destruirla). El primero en ganar 3 rondas gana la partida.

---

## Requisitos

- Python 3.10 o superior
- Tkinter (incluido con Python)
- winsound (incluido con Python en Windows)

---

## Estructura del Proyecto

```
IIProyecto/
│
├── main.py
│
├── clases/
│   ├── jugador.py
│   ├── torre.py
│   ├── unidad.py
│   ├── estructuras.py
│   ├── combate.py
│   ├── archivo_jugadores.py
│   └── musica.py
│
├── ventanas/
│   ├── login.py
│   ├── facciones.py
│   ├── roles.py
│   ├── mapa.py
│   └── ranking.py
│
├── datos/
│   └── jugadores.json
│
└── assets/
    └── sonidos/
        └── musica.wav
```

---

## Instrucciones de Ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/nazth703/defensa-y-asalto-base.git
```

2. Entrar a la carpeta del proyecto:

```bash
cd defensa-y-asalto-base
```

3. Ejecutar el archivo principal:

```bash
python main.py
```

Nota: no ejecutar archivos individuales como mapa.py o login.py directamente, siempre usar main.py.

---

## Como Jugar

1. Login: ambos jugadores inician sesion o se registran.
2. Facciones: cada jugador elige una faccion distinta (Medieval, Naturaleza u Oscura).
3. Roles: un jugador elige Defensor y el otro Atacante.
4. Ronda:
   - El defensor coloca torres y muros en el mapa.
   - El atacante compra y coloca unidades.
   - Se ejecuta el combate automaticamente.
5. El primero en ganar 3 rondas gana la partida.

### Controles

| Accion                    | Control                         |
| ------------------------- | ------------------------------- |
| Colocar elemento          | Click izquierdo en el mapa      |
| Retirar elemento          | Click derecho en el mapa        |
| Pausar juego              | Boton Pausa arriba a la derecha |
| Activar/desactivar musica | Boton Musica en login o pausa   |

---

## Facciones

| Faccion    | Descripcion                            |
| ---------- | -------------------------------------- |
| Medieval   | Muros de piedra y torres de arqueros   |
| Naturaleza | Trampas de raices y torres de druidas  |
| Oscura     | Muros de obsidiana y torres de sombras |

---

## Torres

| Torre        | Costo | Habilidad        |
| ------------ | ----- | ---------------- |
| Torre Basica | $50   | Disparo doble    |
| Torre Pesada | $120  | Dano en area     |
| Torre Magica | $80   | Congela unidades |

---

## Unidades

| Unidad        | Costo | Habilidad            |
| ------------- | ----- | -------------------- |
| Soldado       | $30   | Ataque doble         |
| Tanque        | $100  | Escudo temporal      |
| Unidad Rapida | $50   | Aumento de velocidad |

---

## Repositorio

https://github.com/nazth703/defensa-y-asalto-base
