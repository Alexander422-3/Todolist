from fastapi import HTTPException, status
from database import new_session, TaskModel
from sqlalchemy import select, delete
from schemas import *
from Function import Functions


# class Task:
#     @classmethod
#     async def create(cls, task_name: str):
#         async with new_session() as session:
#             task_field = TaskModel(
#                 task_name=task_name,
#                 task_complete=False
#             )
#             session.add(task_field)
#             await session.flush()
#             await session.commit()
#             return task_field
#     @classmethod
#     async def get(cls, task_id: int):
#         async with new_session() as session:
#             query = select(TaskModel).filter_by(id=task_id)
#             result = await session.execute(query)
#             task = result.scalars().first()
#             if task is None:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail="Данной задачи нет в списке",
#                 )
#             return task
#
#     @classmethod
#     async def get_all(cls):
#         async with new_session() as session:
#             query = select(TaskModel)
#             result = await session.execute(query)
#             tasks = result.scalars().all()
#             return tasks
#
#     @classmethod
#     async def update_complete(cls, task_id: int):
#         async with new_session() as session:
#             query = select(TaskModel).filter_by(id=task_id)
#             result = await session.execute(query)
#             task = result.scalars().first()
#             if task is None:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail="Данной задачи нет в списке",
#                 )
#             task.task_complete = not task.task_complete
#             await session.flush()
#             await session.commit()
#             return task
#
#     @classmethod
#     async def update(cls, task_id: int, task_name: str):
#         async with new_session() as session:
#             query = select(TaskModel).filter_by(id=task_id)
#             result = await session.execute(query)
#             task = result.scalars().first()
#             if task is None:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail="Данной задачи нет в списке",
#                 )
#             task.task_name = task_name
#             await session.flush()
#             await session.commit()
#             return task
#     @classmethod
#     async def delete(cls, task_id: int):
#         async with new_session() as session:
#             query = select(TaskModel).filter_by(id=task_id)
#             result = await session.execute(query)
#             task = result.scalars().first()
#             if task is None:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail="Данной задачи не существует",
#                 )
#             query = delete(TaskModel).filter_by(id=task_id)
#             await session.execute(query)
#             await session.flush()
#             await session.commit()
#             return "Задача успешно удалена"

from fastapi import HTTPException, Request
from sqlalchemy import select, delete
from database import new_session, TaskModel  # Импортируйте вашу модель TaskModel


class Task:
    @classmethod
    async def create(cls, request: Request, task_name: str):
        user_id = await Functions.get_user_id(request)  # Получаем user_id из запроса
        async with new_session() as session:
            task_field = TaskModel(
                task_name=task_name,
                task_complete=False,
                user_id=user_id  # Связываем задачу с пользователем
            )
            session.add(task_field)
            await session.commit()  # Используем commit вместо flush для создания записи
            return task_field

    @classmethod
    async def get(cls, task_id: int):
        async with new_session() as session:
            query = select(TaskModel).filter_by(id=task_id)
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Данной задачи нет в списке",
                )
            return task

    @classmethod
    async def get_all(cls, request: Request):
        user_id = await Functions.get_user_id(request)  # Получаем user_id из запроса
        async with new_session() as session:
            query = select(TaskModel).filter_by(user_id=user_id)  # Фильтруем задачи по user_id
            result = await session.execute(query)
            tasks = result.scalars().all()
            return tasks

    @classmethod
    async def update_complete(cls, request: Request, task_id: int):
        user_id = await Functions.get_user_id(request)  # Получаем user_id из запроса
        async with new_session() as session:
            query = select(TaskModel).filter_by(id=task_id, user_id=user_id)  # Проверяем также user_id
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Данной задачи нет в списке",
                )
            task.task_complete = not task.task_complete
            await session.commit()  # Используем commit для сохранения изменений
            return task

    @classmethod
    async def update(cls, request: Request, task_id: int, task_name: str):
        user_id = await Functions.get_user_id(request)  # Получаем user_id из запроса
        async with new_session() as session:
            query = select(TaskModel).filter_by(id=task_id, user_id=user_id)  # Проверяем также user_id
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Данной задачи нет в списке",
                )
            task.task_name = task_name
            await session.commit()  # Используем commit для сохранения изменений
            return task

    @classmethod
    async def delete(cls, request: Request, task_id: int):
        user_id = await Functions.get_user_id(request)  # Получаем user_id из запроса
        async with new_session() as session:
            query = select(TaskModel).filter_by(id=task_id, user_id=user_id)  # Проверяем также user_id
            result = await session.execute(query)
            task = result.scalars().first()
            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Данной задачи не существует",
                )

            await session.execute(delete(TaskModel).where(TaskModel.id == task.id))
            await session.commit()  # Используем commit для удаления записи

            return "Задача успешно удалена"
