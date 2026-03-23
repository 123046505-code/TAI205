#1. Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

#2. Inicializacion APP
app = FastAPI(
    title="Mi primer API",
    description="Diana Uribe",
    version="1.0.0"
)

#BD ficticia
usuarios = [
    {"id": 1, "nombre": "Eliseo", "edad": 20, "username": "Eliseo", "password": "1234"},
    {"id": 2, "nombre": "Gael", "edad": 22, "username": "Gael", "password": "1234"},
    {"id": 3, "nombre": "julian", "edad": 22, "username": "julian", "password": "1234"},
]

#Modelo de validacion
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")
    username: str = Field(..., min_length=3, max_length=30, example="juan123")
    password: str = Field(..., min_length=4, max_length=50, example="1234")

# configuracion JWT
SECRET_KEY = "mi_clave_super_secreta_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def autenticar_usuario(username: str, password: str):
    for usuario in usuarios:
        if usuario["username"] == username and usuario["password"] == password:
            return usuario
    return None

def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credenciales_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise credenciales_exception

    for usuario in usuarios:
        if usuario["username"] == username:
            return usuario

    raise credenciales_exception


@app.get("/", tags=["Inicio"])
async def inicio():
    return {"mensaje": "API funcionando con JWT"}


@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def consultar_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }


@app.post("/token", tags=["Autenticacion"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar_usuario(form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contrasena incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = crear_access_token(
        data={"sub": usuario["username"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def crear_usuario_endpoint(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
        if usr["username"] == usuario.username:
            raise HTTPException(
                status_code=400,
                detail="El username ya existe"
            )

    usuarios.append(usuario.model_dump())
    return {
        "mensaje": "usuario agregado correctamente",
        "status": "200",
        "usuario": usuario
    }


@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(
    id: int,
    usuario_actualizado: dict,
    usuario_auth: dict = Depends(obtener_usuario_actual)
):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario_actualizado.get("nombre", usr["nombre"])
            usr["edad"] = usuario_actualizado.get("edad", usr["edad"])
            usr["username"] = usuario_actualizado.get("username", usr["username"])
            usr["password"] = usuario_actualizado.get("password", usr["password"])

            return {
                "mensaje": f"Usuario actualizado correctamente por {usuario_auth['username']}",
                "status": "200",
                "usuario": usr
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(
    id: int,
    usuario_auth: dict = Depends(obtener_usuario_actual)
):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado correctamente por {usuario_auth['username']}",
                "status": "200",
                "usuario_eliminado": usr
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")