import pytest
from fastapi.testclient import TestClient

from arena import crear_personaje, simular
from main import app

cliente = TestClient(app)

DATOS = {
    "nombre1": "Guerrero", "vida1": "30", "ataque1": "8", "defensa1": "3",
    "nombre2": "Orco", "vida2": "20", "ataque2": "6", "defensa2": "2",
    "semilla": "2026",
}


def test_ruta_inicio_muestra_el_formulario():
    r = cliente.get("/")
    assert r.status_code == 200
    assert "Simulador de combate" in r.text
    assert 'name="nombre1"' in r.text


def test_combate_por_formulario_con_semilla_fija():
    r = cliente.post("/combatir", data=DATOS)
    assert r.status_code == 200
    assert "Ganador: Guerrero" in r.text
    assert "Simulacion de 1000 combates" in r.text


def test_misma_semilla_da_el_mismo_resultado():
    r1 = cliente.post("/combatir", data=DATOS)
    r2 = cliente.post("/combatir", data=DATOS)
    assert r1.text == r2.text


@pytest.mark.parametrize("campo, valor, mensaje", [
    ("vida1", "0", "la vida debe estar entre 1 y 500"),
    ("ataque2", "-5", "el ataque debe estar entre 0 y 100"),
    ("defensa1", "abc", "deben ser numeros enteros"),
    ("nombre2", "", "El nombre debe tener entre 1 y 20 caracteres"),
    ("nombre2", "guerrero", "nombres distintos"),
    ("semilla", "xyz", "La semilla debe ser un numero entero"),
])
def test_datos_invalidos_devuelven_error_400(campo, valor, mensaje):
    datos = {**DATOS, campo: valor}
    r = cliente.post("/combatir", data=datos)
    assert r.status_code == 400
    assert mensaje in r.text
    assert "Ganador" not in r.text


def test_formulario_vacio_no_rompe_la_app():
    r = cliente.post("/combatir", data={})
    assert r.status_code == 400


def test_crear_personaje_limpia_y_convierte_datos():
    assert crear_personaje("  Mago ", "15", "9", "1") == ("Mago", 15, 9, 1)


def test_simulacion_porcentajes_suman_100_y_el_mas_fuerte_gana_mas():
    fuerte = ("Fuerte", 40, 12, 3)
    debil = ("Debil", 15, 4, 3)
    g1, g2, emp = simular(fuerte, debil, 500, semilla=1)
    assert round(g1 + g2 + emp, 1) == 100.0
    assert g1 > g2
