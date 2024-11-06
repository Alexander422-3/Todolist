from pydantic import BaseModel


class Registr(BaseModel):
    email: str
    password: str
    re_password: str

class Login(BaseModel):
    email: str
    password: str