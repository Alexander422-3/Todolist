from pydantic import BaseModel
class GetTask(BaseModel):
    id: int
    task_name: str
    task_complete: bool
    user_id: int
    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    task_name: str

class UpdateTask(BaseModel):
    id: int
    task_name: str