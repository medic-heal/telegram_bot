from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger())

class Name(Base):
    __tablename__ = 'names'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    surname: Mapped[str] = mapped_column(String(25))
    user_id = mapped_column(ForeignKey('users.tg_id'))

class Score(Base):
    __tablename__ = 'scores'

    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String(25))
    score: Mapped[int] = mapped_column()
    user_id = mapped_column(ForeignKey('users.tg_id'))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
