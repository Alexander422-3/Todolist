from fastapi import APIRouter, status, Response, Request
from schemas import *
from services import UserService

router = APIRouter(tags=["User"], prefix="/user")

@router.post("/register")
async def register(user: Registr):
    return await UserService.registration(user)

@router.put("/login")
async def login(login_data: Login, response: Response):
    return await UserService.login(login_data, response)

@router.post("/logout")
async def logout(response: Response):
    return await UserService.logout(response)
@router.delete("/deleteUser", response_model=str, status_code=status.HTTP_200_OK)
async def delete(user_mail: str):
    return await UserService.delete_user(user_mail)


