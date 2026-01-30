#1.-importacioones
from fastapi import FastAPI
from typing import Optional
import asyncio

#2. Inicializacion APP
app= FastAPI(
    title='Mi primer API',
    description="Diana Maria Uribe",
    version='1.0.0')
#BD ficticia
usuarios=[
    {"id":"1","nombre:":"Diana", "edad":"20"},
    {"id":"1","nombre:":"Gael", "edad":"21"},
    {"id":"1","nombre:":"Ivan", "edad":"38"},
]


#3. Endpoints
@app.get("/", tags=['Inicio'])
async def bien():
    return{"mensaje":"Bienvenido"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenidos():
    return{"mensaje":"bienvenidos"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3) #peticion, consultaBD
    return{"Calificacion":"7.5",
           "estatus":"200"
           }
@app.get("/v1/usuario/{id}", tags=['Parametro'])
async def consultauno(id:int):
    await asyncio.sleep(3) #peticion, consultaBD
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200",
        }

@app.get("/v1/usuarios_op/", tags=['Parametros opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id, "Datos":usuarios }
        return { "Mensaje":"usuario no encontrado" }
    else:
        return { "Aviso":"No se proporciono Id" }