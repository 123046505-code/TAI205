from fastapi import APIRouter, status,HTTPException, Depends
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB



routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    queryUsuarios = db.query(usuarioDB).all()
    return {
        "status": "200",
        "total": len(queryUsuarios),
        "data": queryUsuarios
    }


@routerU.get("/")
async def cosultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
@routerU.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuarios(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    
    suarioNuevo = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(suarioNuevo)
    db.commit()
    db.refresh(suarioNuevo)
    return {
        "mensaje": "Usuario agregado correctamente",
        "status": "200",
        "usuario": suarioNuevo
    }
    
@routerU.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    usuarios.append(usuario.dict())
    return{
        "mensaje":"usuario agregado correctamente",
        "status":"200",
        "usuario":usuario
    }
    
@routerU.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario_actualizado.get("nombre", usr["nombre"])
            usr["edad"] = usuario_actualizado.get("edad", usr["edad"])
            
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usr
            }
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@routerU.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, userAuth:str=Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado correctamente por {userAuth}",
                "status": "200",
                "usuario_eliminado": usr
            }
            
    raise HTTPException(status_code=404, detail="Usuario no encontrado")