import random

import pytest

from rpg import Dado, Personaje, calcular_dano, combate


class DadoTrucado:
    def __init__(self, tiradas):
        self.tiradas = list(tiradas)

    def tirar(self):
        return self.tiradas.pop(0)


@pytest.fixture
def guerrero():
    return Personaje("Guerrero", vida=30, ataque=8, defensa=3)


@pytest.fixture
def orco():
    return Personaje("Orco", vida=20, ataque=6, defensa=2)


@pytest.mark.parametrize("caras", [6, 12, 20])
def test_dado_siempre_cae_dentro_del_rango(caras):
    dado = Dado(caras, random.Random(7))
    tiradas = [dado.tirar() for _ in range(1000)]
    assert min(tiradas) == 1
    assert max(tiradas) == caras


def test_misma_semilla_mismas_tiradas():
    a = Dado(20, random.Random(42))
    b = Dado(20, random.Random(42))
    assert [a.tirar() for _ in range(10)] == [b.tirar() for _ in range(10)]


def test_dado_con_menos_de_dos_caras_es_invalido():
    with pytest.raises(ValueError):
        Dado(1)


@pytest.mark.parametrize(
    "tirada, esperado",
    [(1, 0), (2, 6), (14, 6), (15, 8), (19, 8), (20, 12)],
)
def test_dano_segun_la_tirada(guerrero, orco, tirada, esperado):
    assert calcular_dano(guerrero, orco, tirada) == esperado


def test_dano_minimo_es_uno_aunque_la_defensa_sea_mayor(orco):
    tanque = Personaje("Tanque", vida=50, ataque=1, defensa=10)
    assert calcular_dano(orco, tanque, 10) == 1


def test_la_vida_nunca_queda_negativa(orco):
    orco.recibir_dano(500)
    assert orco.vida == 0
    assert not orco.esta_vivo()


def test_personaje_sin_vida_inicial_es_invalido():
    with pytest.raises(ValueError):
        Personaje("Fantasma", vida=0, ataque=1, defensa=1)


def test_combate_con_dados_controlados(guerrero, orco):
    ganador, registro = combate(guerrero, orco, DadoTrucado([20, 10, 15]))
    assert ganador == "Guerrero"
    assert [fila[3] for fila in registro] == [12, 3, 8]
    assert orco.vida == 0
    assert guerrero.vida == 27


def test_combate_sin_ganador_si_se_acaban_los_turnos(guerrero, orco):
    ganador, registro = combate(guerrero, orco, DadoTrucado([1] * 10), max_turnos=10)
    assert ganador is None
    assert len(registro) == 10
    assert guerrero.vida == 30 and orco.vida == 20
