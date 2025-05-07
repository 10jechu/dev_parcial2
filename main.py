from fastapi import FastAPI, Depends, Path, Query, HTTPException
from contextlib import asynccontextmanager
from data.models import UserSQL, TaskSQL, UserStatus, TaskStatus, UserBase, TaskBase, UpdatedUser, TaskUpdated
from connection_db import get_db_session, init_db
from sqlmodel.ext.asyncio.session import AsyncSession
import operations_db as crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Inicializa la base de datos al inicio
    yield
    # Aquí podrías añadir código para cleanup al shutdown, si lo necesitas

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/tasks/", response_model=TaskSQL, tags=["Create Task"])
async def create_task_endpoint(task: TaskBase, session: AsyncSession = Depends(get_db_session)):
    # Convertir TaskBase a TaskSQL
    task_sql = TaskSQL(**task.dict())
    return await crud.create_task_sql(session, task_sql)

@app.get("/tasks/", response_model=list[TaskSQL], tags=["List Task"])
async def list_tasks_endpoint(session: AsyncSession = Depends(get_db_session)):
    return await crud.list_tasks(session)

@app.get("/tasks/{task_id}", response_model=TaskSQL, tags=["List Task"])
async def list_tasks_by_id_endpoint(task_id: int, session: AsyncSession = Depends(get_db_session)):
    try:
        task = await crud.get_task(session, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        print(f"Error: {str(e)}")  # Imprime el error en la consola
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/users/", response_model=UserSQL, tags=["Create User"])
async def create_user_endpoint(user: UserBase, session: AsyncSession = Depends(get_db_session)):
    # Convertir UserBase a UserSQL
    user_sql = UserSQL(**user.dict())
    return await crud.create_user_sql(session, user_sql)

@app.get("/users/", response_model=list[UserSQL], tags=["List User"])
async def list_users_endpoint(session: AsyncSession = Depends(get_db_session)):
    return await crud.list_users(session)

@app.get("/users/inactivo", response_model=list[UserSQL], tags=["Get Inactive Users"])
async def list_inactive_users_endpoint(session: AsyncSession = Depends(get_db_session)):
    return await crud.list_inactive_users(session)

@app.get("/users/inactivo&premium", response_model=list[UserSQL], tags=["Get Inactive & Premium Users"])
async def list_inactive_and_premium_users_endpoint(session: AsyncSession = Depends(get_db_session)):
    return await crud.list_inactive_and_premium(session)

@app.get("/users/{user_id}", response_model=UserSQL, tags=["List User"])
async def list_users_by_id_endpoint(user_id: int, session: AsyncSession = Depends(get_db_session)):
    user = await crud.get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=UserSQL, tags=["Update User"])
async def update_user_endpoint(user_id: int, user_update: UpdatedUser, session: AsyncSession = Depends(get_db_session)):
    updated_user = await crud.update_user(session, user_id, user_update.dict(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.patch("/tasks/{task_id}", response_model=TaskSQL, tags=["Update Task"])
async def update_task_endpoint(task_id: int, task_update: TaskUpdated, session: AsyncSession = Depends(get_db_session)):
    updated_task = await crud.update_task(session, task_id, task_update.dict(exclude_unset=True))
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.patch("/users/{user_id}/premium", response_model=UserSQL, tags=["Update User"])
async def convert_user_to_premium_endpoint(user_id: int, session: AsyncSession = Depends(get_db_session)):
    updated_user = await crud.convert_user_to_premium(session, user_id, {"premium": True})
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.patch("/users/{user_id}/status", response_model=UserSQL, tags=["Update User"])
async def update_user_status_endpoint(
    user_id: int = Path(..., description="ID del usuario a actualizar"),
    new_status: UserStatus = Query(..., description="Nuevo estado: a (activo), i (inactivo), d (eliminado)"),
    session: AsyncSession = Depends(get_db_session)
):
    updated_user = await crud.convert_user_status(session, user_id, new_status)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.patch("/tasks/{task_id}/status", response_model=TaskSQL, tags=["Update Task"])
async def update_task_status_endpoint(
    task_id: int = Path(..., description="ID del task a actualizar"),
    new_status: TaskStatus = Query(..., description="Nuevo estado: p (Pendiente), ip (en ejecucion), f (completada), c (cancelada)"),
    session: AsyncSession = Depends(get_db_session)
):
    updated_task = await crud.convert_task_status(session, task_id, new_status)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Forzar despliegue para Clever Cloud

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
