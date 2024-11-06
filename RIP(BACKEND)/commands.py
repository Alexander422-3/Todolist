import click
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker
from database import TaskModel


engine = create_engine("sqlite:///./sql_app.db")
new_session = sessionmaker(engine, expire_on_commit=False)

@click.group()
def default_command():
    """Команды для управления задачами."""
    pass

def display_menu():
    """Отображение меню выбора команд."""
    options = [
        "1. Вывести все задачи",
        "2. Найти задачу по ID",
        "3. Создать новую задачу",
        "4. Обновить статус задачи",
        "5. Удалить задачу",
        "0. Выход"
    ]
    click.echo("\n".join(options))

def get_task_id():
    """Запрос идентификатора задачи у пользователя."""
    return click.prompt("Введите ID задачи", type=int)

def get_task_name(default=None):
    """Запрос имени задачи у пользователя."""
    return click.prompt("Введите название задачи", default=default)

@default_command.command()
def run():
    """Запуск меню команд."""
    while True:
        display_menu()
        choice = click.prompt("Выберите команду", type=int)

        if choice == 1:
            while True:
                get_all_tasks()
                if click.confirm("Хотите выбрать другую команду?", default=True):
                    break
        elif choice == 2:
            while True:
                task_id = get_task_id()
                get_task(task_id)
                if click.confirm("Хотите выбрать другую команду?", default=True):
                    break
        elif choice == 3:
            while True:
                task_name = get_task_name()
                create_task(task_name)
                if click.confirm("Хотите выбрать другую команду?", default=True):
                    break
        elif choice == 4:
            while True:
                task_id = get_task_id()
                complete_task(task_id)
                if click.confirm("Хотите выбрать другую команду?", default=True):
                    break
        elif choice == 5:
            while True:
                task_id = get_task_id()
                delete_task(task_id)
                if click.confirm("Хотите выбрать другую команду?", default=True):
                    break
        elif choice == 0:
            click.echo("Выход...")
            break
        else:
            click.echo("Неверный выбор. Попробуйте снова.")
def get_all_tasks():
    """Вывод всех задач на экран."""
    with new_session() as session:
        query = select(TaskModel)
        result = session.execute(query)
        tasks = result.scalars().all()
        for task in tasks:
            click.echo(f'id={task.id}, название={task.task_name}, статуc={task.task_complete}')

def get_task(task_id):
    """Найти задачу по её id."""
    with new_session() as session:
        query = select(TaskModel).filter_by(id=task_id)
        result = session.execute(query)
        task = result.scalars().first()
        if task:
            click.echo(f'id={task.id}, название={task.task_name}, статуc={task.task_complete}')
        else:
            click.echo("Задача не найдена.")

def create_task(task_name):
    """Создать новую задачу."""
    with new_session() as session:
        task_field = TaskModel(
            task_name=task_name,
            task_complete=False
        )
        session.add(task_field)
        session.commit()
        click.echo(f'Задача создана: id={task_field.id}, название={task_field.task_name}, статуc={task_field.task_complete}')

def complete_task(task_id):
    """Обновить статус задачи."""
    with new_session() as session:
        query = select(TaskModel).filter_by(id=task_id)
        result = session.execute(query)
        task = result.scalars().first()
        if task:
            task.task_complete = not task.task_complete
            session.commit()
            click.echo(f'Статус задачи обновлен: id={task.id}, название={task.task_name}, статуc={task.task_complete}')
        else:
            click.echo("Задача не найдена.")

def delete_task(task_id):
    """Удалить задачу."""
    with new_session() as session:
        query = select(TaskModel).filter_by(id=task_id)
        result = session.execute(query)
        task = result.scalars().first()
        if not task:
            click.echo('Задача не найдена')
            return
        session.execute(delete(TaskModel).filter_by(id=task_id))
        session.commit()
        click.echo("Задача успешно удалена.")

if __name__ == '__main__':
    default_command()

