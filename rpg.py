import random


class Dado:
    def __init__(self, caras=20, generador=None):
        if caras < 2:
            raise ValueError("Un dado necesita al menos 2 caras")
        self.caras = caras
        self.generador = generador or random.Random()

    def tirar(self):
        return self.generador.randint(1, self.caras)


class Personaje:
    def __init__(self, nombre, vida, ataque, defensa):
        if vida <= 0:
            raise ValueError("La vida inicial debe ser mayor que cero")
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    def esta_vivo(self):
        return self.vida > 0

    def recibir_dano(self, cantidad):
        self.vida = max(0, self.vida - cantidad)


def calcular_dano(atacante, defensor, tirada):
    if tirada == 1:
        return 0
    base = max(1, atacante.ataque - defensor.defensa)
    if tirada == 20:
        return base * 2
    if tirada >= 15:
        return base + 2
    return base


def combate(jugador1, jugador2, dado, max_turnos=100):
    registro = []
    atacante, defensor = jugador1, jugador2
    for turno in range(1, max_turnos + 1):
        tirada = dado.tirar()
        dano = calcular_dano(atacante, defensor, tirada)
        defensor.recibir_dano(dano)
        registro.append((turno, atacante.nombre, tirada, dano, defensor.vida))
        if not defensor.esta_vivo():
            return atacante.nombre, registro
        atacante, defensor = defensor, atacante
    return None, registro
