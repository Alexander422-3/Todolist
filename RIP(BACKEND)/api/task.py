# from fastapi import APIRouter, status
# from schemas import GetTask, TaskCreate, UpdateTask
# from services import Task
#
# router = APIRouter(tags=["Task"], prefix="/task")
#
# @router.post("/createtask", response_model=GetTask, status_code=status.HTTP_200_OK)
# async def create(task: TaskCreate):
#     return await Task.create(task.task_name)
#
# @router.get("/getAlltasks", response_model=list[GetTask], status_code=status.HTTP_200_OK)
# async def get_all():
#     return await Task.get_all()
#
# @router.get("/getOnetask/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
# async def get(task_id: int):
#     return await Task.get(task_id)
#
# @router.put("/update_complete/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
# async def update_complete(task_id: int):
#     return await Task.update_complete(task_id)
#
# @router.put("/update_task/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
# async def update_task(task_id: int, task: TaskCreate):
#     return await Task.update(task_id, task.task_name)
#
#
# @router.delete("/deleteTask/{task_id}", response_model=str, status_code=status.HTTP_200_OK)
# async def delete(task_id: int):
#     return await Task.delete(task_id)

from fastapi import APIRouter, Depends, Request, status
from schemas import GetTask, TaskCreate  # Импортируйте ваши Pydantic модели
from services import Task  # Импортируйте ваш класс Task

router = APIRouter(tags=["Tasks"], prefix="/tasks")

@router.post("/createtask", response_model=GetTask, status_code=status.HTTP_200_OK)
async def create(request: Request, task: TaskCreate):
    return await Task.create(request, task.task_name)

@router.get("/getAlltasks", response_model=list[GetTask], status_code=status.HTTP_200_OK)
async def get_all(request: Request):
    return await Task.get_all(request)

@router.get("/getOnetask/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def get(task_id: int, request: Request):
    return await Task.get(task_id)

@router.put("/update_complete/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def update_complete(task_id: int, request: Request):
    return await Task.update_complete(request, task_id)

@router.put("/update_task/{task_id}", response_model=GetTask, status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task: TaskCreate, request: Request):
    return await Task.update(request, task_id, task.task_name)

@router.delete("/deleteTask/{task_id}", response_model=str, status_code=status.HTTP_200_OK)
async def delete(task_id: int, request: Request):
    return await Task.delete(request, task_id)
