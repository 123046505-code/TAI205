#1. Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios



#2. Inicializacion APP
app= FastAPI(
    title="Mi primer API", 
    description="Diana Maria Uribe",
    version="1.0"
    )

app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
