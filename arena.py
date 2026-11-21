import random

from rpg import Dado, Personaje, combate


def crear_personaje(nombre, vida, ataque, defensa):
    """Valida los datos del formulario y devuelve una tupla (nombre, vida, ataque, defensa)."""
    nombre = (nombre or "").strip()
    if not nombre or len(nombre) > 20:
        raise ValueError("El nombre debe tener entre 1 y 20 caracteres")
    try:
        vida, ataque, defensa = int(vida), int(ataque), int(defensa)
    except (TypeError, ValueError):
        raise ValueError(f"{nombre}: vida, ataque y defensa deben ser numeros enteros")
    if not 1 <= vida <= 500:
        raise ValueError(f"{nombre}: la vida debe estar entre 1 y 500")
    if not 0 <= ataque <= 100:
        raise ValueError(f"{nombre}: el ataque debe estar entre 0 y 100")
    if not 0 <= defensa <= 100:
        raise ValueError(f"{nombre}: la defensa debe estar entre 0 y 100")
    return (nombre, vida, ataque, defensa)


def leer_semilla(texto):
    """Semilla opcional: vacio -> None."""
    texto = (texto or "").strip()
    if texto == "":
        return None
    try:
        return int(texto)
    except ValueError:
        raise ValueError("La semilla debe ser un numero entero")


def efecto(tirada):
    if tirada == 1:
        return "FALLO"
    if tirada == 20:
        return "CRITICO"
    if tirada >= 15:
        return "golpe fuerte"
    return "golpe normal"


def pelear(datos1, datos2, semilla=None):
    """Un combate. Devuelve (ganador, filas) con el efecto de cada tirada."""
    a, b = Personaje(*datos1), Personaje(*datos2)
    ganador, registro = combate(a, b, Dado(20, random.Random(semilla)))
    filas = [
        {"turno": t, "atacante": at, "tirada": ti, "efecto": efecto(ti),
         "dano": d, "vida": v}
        for t, at, ti, d, v in registro
    ]
    return ganador, filas


def simular(datos1, datos2, n=1000, semilla=None):
    """Repite el combate n veces. Devuelve porcentajes (gana1, gana2, empate)."""
    dado = Dado(20, random.Random(semilla))
    g1 = g2 = 0
    for _ in range(n):
        ganador, _ = combate(Personaje(*datos1), Personaje(*datos2), dado)
        if ganador == datos1[0]:
            g1 += 1
        elif ganador == datos2[0]:
            g2 += 1
    emp = n - g1 - g2
    return (round(100 * g1 / n, 1), round(100 * g2 / n, 1), round(100 * emp / n, 1))
