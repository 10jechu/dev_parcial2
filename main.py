from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from data.models import Cliente
from typing import List
from operations.operations_db import create_cliente, read_clientes, update_cliente, delete_cliente
from utils.connection_db import init_db, get_session
from sqlmodel.ext.asyncio.session import AsyncSession

# Manejador de lifespan para inicializar la base de datos
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# Crear la aplicación FastAPI con el manejador de lifespan
app = FastAPI(title="API de Clientes", lifespan=lifespan)

# Operaciones CRUD como rutas
@app.post("/clientes/", response_model=Cliente)
async def api_create_cliente(cliente: Cliente, db: AsyncSession = Depends(get_session)):
    return await create_cliente(db, cliente)

@app.get("/clientes/", response_model=List[Cliente])
async def api_read_clientes(db: AsyncSession = Depends(get_session)):
    return await read_clientes(db)

@app.put("/clientes/{cliente_id}", response_model=Cliente)
async def api_update_cliente(cliente_id: int, cliente_actualizado: Cliente, db: AsyncSession = Depends(get_session)):
    return await update_cliente(db, cliente_id, cliente_actualizado)

@app.delete("/clientes/{cliente_id}")
async def api_delete_cliente(cliente_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_cliente(db, cliente_id)

# Ruta de prueba (opcional, para verificar el servidor)
@app.get("/")
async def read_root():
    return {"message": "Servidor ejecutándose correctamente"}

# Ejecutar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)