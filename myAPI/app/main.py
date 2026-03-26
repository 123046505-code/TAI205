#1. Importaciones
from fastapi import FastAPI
from app.routers.varios import routerV
from app.routers.usuarios import routerU
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

#2. Inicializacion APP
app= FastAPI(
    title="Mi primer API", 
    description="Diana Maria Uribe",
    version="1.0"
    )

app.include_router(routerU)
app.include_router(routerV)
