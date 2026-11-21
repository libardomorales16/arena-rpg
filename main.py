from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from arena import crear_personaje, leer_semilla, pelear, simular

BASE = Path(__file__).parent
app = FastAPI(title="Arena RPG")
plantillas = Jinja2Templates(directory=str(BASE / "templates"))

DEFECTO = {
    "nombre1": "Guerrero", "vida1": "30", "ataque1": "8", "defensa1": "3",
    "nombre2": "Orco", "vida2": "20", "ataque2": "6", "defensa2": "2",
    "semilla": "",
}


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return plantillas.TemplateResponse(
        request, "index.html", {"form": DEFECTO, "error": None})


@app.post("/combatir", response_class=HTMLResponse)
def combatir(
    request: Request,
    nombre1: str = Form(""), vida1: str = Form(""),
    ataque1: str = Form(""), defensa1: str = Form(""),
    nombre2: str = Form(""), vida2: str = Form(""),
    ataque2: str = Form(""), defensa2: str = Form(""),
    semilla: str = Form(""),
):
    form = {
        "nombre1": nombre1, "vida1": vida1, "ataque1": ataque1, "defensa1": defensa1,
        "nombre2": nombre2, "vida2": vida2, "ataque2": ataque2, "defensa2": defensa2,
        "semilla": semilla,
    }
    try:
        p1 = crear_personaje(nombre1, vida1, ataque1, defensa1)
        p2 = crear_personaje(nombre2, vida2, ataque2, defensa2)
        if p1[0].lower() == p2[0].lower():
            raise ValueError("Los dos personajes deben tener nombres distintos")
        sem = leer_semilla(semilla)
    except ValueError as e:
        return plantillas.TemplateResponse(
            request, "index.html", {"form": form, "error": str(e)}, status_code=400)

    ganador, filas = pelear(p1, p2, sem)
    n = 1000
    pct1, pct2, pctE = simular(p1, p2, n, sem)
    return plantillas.TemplateResponse(request, "resultado.html", {
        "p1": p1, "p2": p2, "ganador": ganador, "filas": filas,
        "n": n, "pct1": pct1, "pct2": pct2, "pctE": pctE, "semilla": sem,
    })
