
from fastapi import FastAPI,status,HTTPException, Depends

from fastapi import FastAPI
from typing import Optional
import asyncio

app= FastAPI()
app= FastAPI(
    title='Sistema de reserva de hospedaje',
    description="Diana Maria Uribe",
    version='1.0.0')

Reservas=[
    {"id":"1","huesped:":"Diana", "fecha entrada":"25/1/26", "fecha salida":"27/1/26", "tipo abitacion":"sencilla"},
    {"id":"2","huesped:":"Gael","fecha entrada":"25/1/26", "fecha salida":"27/1/26", "tipo abitacion":"suite"},
    {"id":"3","huesped:":"eliseo", "fecha entrada":"25/1/26", "fecha salida":"27/1/26", "tipo abitacion":"doble"},
]


@app.post("/v1/usuarios/", tags=['crear reserva'])
async def crear_reserva(Reservas:crear_reserva):

    for usr in Reservas:
        if usr["id"] == Reservas.id:
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    Reservas.append(Reservas.dict())
    return{
        "mensaje":"reserva agregado correctamente",
        "status":"200",
        "usuario":usuario
    }









































