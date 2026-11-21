import random
import sys

from rpg import Dado, Personaje, combate


def main():
    semilla = int(sys.argv[1]) if len(sys.argv) > 1 else None
    guerrero = Personaje("Guerrero", vida=30, ataque=8, defensa=3)
    orco = Personaje("Orco", vida=20, ataque=6, defensa=2)
    ganador, registro = combate(guerrero, orco, Dado(20, random.Random(semilla)))
    print("=== COMBATE RPG: Guerrero vs Orco ===")
    for turno, atacante, tirada, dano, vida_rival in registro:
        if tirada == 1:
            efecto = "FALLO"
        elif tirada == 20:
            efecto = "CRITICO"
        elif tirada >= 15:
            efecto = "golpe fuerte"
        else:
            efecto = "golpe normal"
        print(f"Turno {turno:>2} | {atacante:<8} saca {tirada:>2} ({efecto:<12}) -> {dano:>2} de dano | vida del rival: {vida_rival}")
    print(f"Ganador: {ganador or 'empate por limite de turnos'}")


if __name__ == "__main__":
    main()
