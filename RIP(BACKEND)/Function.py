from fastapi import HTTPException, Request
import jwt

SECRET_KEY = "manilovefishing"

class Functions:
    @staticmethod
    async def get_user_id(request: Request):
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(status_code=401, detail="Необходима авторизация")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("id")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Не удалось извлечь user_id из токена")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Неверный токен")

        return user_id


