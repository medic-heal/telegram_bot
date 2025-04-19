from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# Создание асинхронного движка для подключения к SQLite базе данных
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

# Создание фабрики асинхронных сессий для работы с базой данных
async_session = async_sessionmaker(engine)

# Базовый класс для всех моделей с поддержкой асинхронных атрибутов
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Модель пользователя Telegram
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True) # Уникальный идентификатор записи
    tg_id = mapped_column(BigInteger()) # Telegram ID пользователя

# Модель имени пользователя
class Name(Base):
    __tablename__ = 'names'

    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(25)) # Имя пользователя (до 25 символов)
    surname: Mapped[str] = mapped_column(String(25)) # Фамилия пользователя (до 25 символов)
    user_id = mapped_column(ForeignKey('users.tg_id')) # Внешний ключ, связывающий имя с пользователем по tg_id

# Модель результатов пользователя
class Score(Base):
    __tablename__ = 'scores'

    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String(25))  # Название предмета
    score: Mapped[int] = mapped_column() # Значение очков
    user_id = mapped_column(ForeignKey('users.tg_id')) # Внешний ключ, связывающий запись с пользователем по tg_id

# Асинхронная функция для создания всех таблиц в базе данных
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
