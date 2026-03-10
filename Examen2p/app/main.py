
from fastapi import FastAPI,status,HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from pydantic import BaseModel,Field

app= FastAPI()
app= FastAPI(
    title='Sistema de reserva de hospedaje',
    description="Diana Maria Uribe",
    version='1.0.0')

Reservas=[
    {"id":"1","huesped:":"Diana", "fecha entrada":"25/1/26", "fecha salida":"27/1/26", "tipo habitacion":"sencilla"},
    {"id":"2","huesped:":"Gael","fecha entrada":"25/1/26", "fecha salida":"27/1/26", "tipo habitacion":"suite"},
    {"id":"3","huesped:":"eliseo", "fecha entrada":"25/1/26", "fecha salida":"27/1/26", "tipo habitacion":"doble"},
]

#SEGURIDAD

class crear_usuario(BaseModel):

    id: int = Field( ... ,gt=0, description="Identificador de usuario")

seguridad = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):

    userAuth= secrets.compare_digest(credenciales.username,"hotel")

    passAuth= secrets.compare_digest(credenciales.password,"r2026")

    if not (userAuth and passAuth ):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "credenciales no autorizadas"
        )
    return credenciales.username



#CREAR RESERVA
@app.post("/v1/Reserva/", tags=['crear reserva'])
async def crear_reserva(id: int, userAuth:str=Depends(verificar_peticion)):

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
        "reserva":Reservas
    }

# ELIMINAR/CANCELAR RESERVA
@app.delete("/v1/Reservas/{id}", tags=['eliminar reserva'])
async def eliminar_Reserva(id: int, userAuth:str=Depends(verificar_peticion)):

    for usr in Reservas:
        if usr["id"] == id:
            Reservas.remove(usr)
            return {
                "mensaje": f"Reserva eliminada correctamente por {userAuth}",
                "status": "200",
                "reserva_eliminado": usr
            }
            
    raise HTTPException(status_code=404, detail="Reserva no encontrada")


# MOSTRAR RESERVAS
@app.get("/v1/Reservas/", tags=['Listar reservas'])
async def cosultaT():

    return{
        "status":"200",
        "total": len(Reservas),
        "data":Reservas
    }
    






















































