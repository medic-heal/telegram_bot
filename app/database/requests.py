from app.database.models import async_session
from app.database.models import User, Name, Score
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

# Функция добавления нового пользователя в базу
async def set_user(tg_id: int):
    async with async_session() as session:
        # Проверка, существует ли пользователь с таким tg_id
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            # Если нет — создаём новую запись
            new_user = User(tg_id=tg_id)
            session.add(new_user)
            await session.commit()
        
# Функция для записи имени и фамилии пользователя
async def set_name(tg_id, name, surname):
    async with async_session() as session:
        # Проверка, есть ли уже запись с именем по данному tg_id
        user = await session.scalar(select(Name).where(Name.user_id == tg_id))

        if not user:
            # Если нет — создаём новую запись
            new_name = Name(user_id=tg_id, name=name, surname=surname)
            session.add(new_name)
            await session.commit()

# Функция для добавления нового результата пользователя
async def set_score(tg_id, item_name, score):
    async with async_session() as session:
        new_score = Score(user_id=tg_id, item_name=item_name, score=score)
        session.add(new_score)
        await session.commit()

# Получение всех результатов пользователя 
async def get_user_scores(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(Score.item_name, Score.score).where(Score.user_id == tg_id))
        scores = result.all()
        return scores if scores else None

# Проверка наличия регистрации у пользователя
async def is_user_registered(tg_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Name).where(Name.user_id == tg_id))
        return result is not None

# Получение записи с именем и фамилией пользователя    
async def get_user_register(tg_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Name).where(Name.user_id == tg_id))
        return result if result else None

# Удаление всех результатов пользователя
async def delete_user_scores(tg_id: int):
    async with async_session() as session:
        stmt = delete(Score).where(Score.user_id == tg_id)
        await session.execute(stmt)
        await session.commit()

# Полная очистка всех данных в базе
async def clear_database():
    async with async_session() as session:
        await session.execute(delete(Score))
        await session.execute(delete(Name))
        await session.execute(delete(User))
        await session.commit()

# Получение всех оценок всех пользователей вместе с их именами
async def get_all_students_scores():
    async with async_session() as session:
        result = await session.execute(
            select(Name.name, Name.surname, Score.item_name, Score.score)
            .join(Score, Name.user_id == Score.user_id, isouter=True)
        )
        scores = result.all()
        return scores if scores else []
