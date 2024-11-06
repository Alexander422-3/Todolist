from fastapi import HTTPException, status, Response, Request
from database import new_session, User
from schemas import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
import bcrypt
import jwt

SECRET_KEY = "manilovefishing"

class UserService:
    @classmethod
    async def registration(cls, user: Registr):
        async with new_session() as db:
            if user.password != user.re_password:
                raise HTTPException(status_code=400, detail="Пароли не совпадают")

            result = await db.execute(select(User).where(User.email == user.email))
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

            # Хешируем пароль
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # token_data = {
            #     "mail": user.email
            # }
            # token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

            # Создаем нового пользователя и добавляем его в сессию
            new_user = User(email=user.email, password=hashed_password)
            db.add(new_user)

            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при сохранении пользователя")

            return {
                "email": new_user.email,
                #"token": token,
                "message": "Пользователь успешно зарегистрирован."
            }

    @classmethod
    async def login(cls, login_data: Login, response: Response):
        async with new_session() as db:
            result = await db.execute(select(User).where(User.email == login_data.email))
            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=400, detail="Неверный email или пароль")

            if not bcrypt.checkpw(login_data.password.encode('utf-8'), user.password.encode('utf-8')):
                raise HTTPException(status_code=400, detail="Неверный email или пароль")

            token_data = {
                "id": user.id
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
            response.set_cookie(key="token", value=token, httponly=True, secure=False)
            return {
                "email": user.email,
                "token": token,
                "message": "Пользователь успешно авторизован."
            }

    @classmethod
    async def logout(cls, response: Response):
        response.delete_cookie(key="token")
        return {"message": "Пользователь успешно вышел из системы."}


    @classmethod
    async def delete_user(cls, user_email: str):
        async with new_session() as db:
            result = await db.execute(select(User).where(User.email == user_email))
            user_to_delete = result.scalars().first()

            if not user_to_delete:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            await db.delete(user_to_delete)

            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(status_code=500, detail="Ошибка при удалении пользователя")

            return "Пользователь успешно удален."



#
            # new_token = Token(token=token)
            # db.add(new_token)
            # await db.commit()

            #response.set_cookie(key="token", value=token, httponly=True)
# async def login(cls, login_data: Login, response: Response):
    #     async with new_session() as db:
    #         result = await db.execute(select(User).where(User.email == login_data.email))
    #         user = result.scalars().first()
    #
    #         if not user:
    #             raise HTTPException(status_code=400, detail="Неверный email или пароль")
    #
    #         if not bcrypt.checkpw(login_data.password.encode('utf-8'), user.password.encode('utf-8')):
    #             raise HTTPException(status_code=400, detail="Неверный email или пароль")
    #
    #         token_data = {
    #             "sub": user.email,
    #             "id": user.id
    #         }
    #         token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    #
    #         # Установка cookies с токеном
    #         response.set_cookie(key="token", value=token, httponly=True)
    #
    #         return {
    #             "email": user.email,
    #             "token": token,
    #             "message": "Пользователь успешно авторизован."
    #         }