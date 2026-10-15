from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request
from estructuras import ListaCircular

app = FastAPI(
    title="Estructuras de DATOS - Taller Listas Circulares",
    description="API utilizando Lista Circular Simplemente Enlazada para Turnos",
    version="1.0"
)

templates = Jinja2Templates(directory="templates")
lista_turnos = ListaCircular()

class Persona(BaseModel):
    nombre: str
    identificacion: str

class PasosRequest(BaseModel):
    pasos: int

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/persona/agregar")
def agregar_persona(persona: Persona):
    if lista_turnos.buscar(persona.identificacion):
        raise HTTPException(status_code=400, detail="La identificación ya se encuentra registrada.")
    lista_turnos.agregar(persona.nombre, persona.identificacion)
    return {"mensaje": "Persona agregada exitosamente", "total": lista_turnos.contar()}

@app.get("/personas/mostrar")
def mostrar_personas():
    return {
        "total": lista_turnos.contar(),
        "turno_actual": lista_turnos.obtener_turno_actual().nombre if lista_turnos.obtener_turno_actual() else None,
        "elementos": lista_turnos.mostrar()
    }

@app.get("/persona/buscar/{identificacion}")
def buscar_persona(identificacion: str):
    nodo = lista_turnos.buscar(identificacion)
    if not nodo:
        raise HTTPException(status_code=404, detail="Persona no encontrada en la lista circular.")
    return {
        "nombre": nodo.nombre,
        "identificacion": nodo.identificacion,
        "turnos_atendidos": nodo.turnos_atendidos
    }

@app.delete("/persona/eliminar/{identificacion}")
def eliminar_persona(identificacion: str):
    eliminado = lista_turnos.eliminar(identificacion)
    if not eliminado:
        raise HTTPException(status_code=404, detail="No se pudo eliminar, la persona no existe.")
    return {"mensaje": "Persona eliminada correctamente", "total": lista_turnos.contar()}

@app.get("/turno/actual")
def ver_turno_actual():
    actual = lista_turnos.obtener_turno_actual()
    if not actual:
        return {"mensaje": "La lista está vacía, no hay turnos activos."}
    return {
        "nombre": actual.nombre,
        "identificacion": actual.identificacion,
        "turnos_atendidos": actual.turnos_atendidos
    }

@app.post("/turno/siguiente")
def siguiente_turno():
    actual = lista_turnos.siguiente_turno()
    if not actual:
        raise HTTPException(status_code=400, detail="La lista está vacía.")
    return {"mensaje": "Turno avanzado", "turno_actual": actual.nombre}

@app.post("/turno/anterior")
def anterior_turno():
    actual = lista_turnos.anterior_turno()
    if not actual:
        raise HTTPException(status_code=400, detail="La lista está vacía.")
    return {"mensaje": "Turno retrocedido", "turno_actual": actual.nombre}

@app.post("/turno/avanzar_multiples")
def avanzar_multiples(data: PasosRequest):
    actual = lista_turnos.avanzar_varios(data.pasos)
    if not actual:
        raise HTTPException(status_code=400, detail="La lista está vacía.")
    return {"mensaje": f"Se avanzaron {data.pasos} turnos", "turno_actual": actual.nombre}