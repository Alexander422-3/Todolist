from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

engine = create_async_engine("sqlite+aiosqlite:///./sql_app.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    tasks = relationship("TaskModel", back_populates="user")
class TaskModel(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String, nullable=False)
    task_complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="tasks")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



#class Model(DeclarativeBase):
    #pass

# class TaskModel(Model):
#     __tablename__ = "task"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     description: Mapped[str]
#     complete: Mapped[bool]
#
#async def create_tables():
    #async with engine.begin() as conn:
        #await conn.run_sync(Model.metadata.create_all)
