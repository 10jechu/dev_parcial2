from sqlmodel import select
from data.models import Cliente
from fastapi import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

async def create_cliente(db: AsyncSession, cliente: Cliente):
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    print(f"Cliente creado con id: {cliente.id}")  # Log para depuración
    return cliente

async def read_clientes(db: AsyncSession):
    statement = select(Cliente)
    result = await db.exec(statement)
    return result.all()

async def update_cliente(db: AsyncSession, cliente_id: int, cliente_actualizado: Cliente):
    cliente = await db.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente_data = cliente_actualizado.dict(exclude_unset=True)
    for key, value in cliente_data.items():
        setattr(cliente, key, value)
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    return cliente

async def delete_cliente(db: AsyncSession, cliente_id: int):
    cliente = await db.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    await db.delete(cliente)
    await db.commit()
    return {"message": "Cliente eliminado correctamente"}