from contextlib import asynccontextmanager

import config
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_async_engine(config.PG_DSN, echo=True)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


class People(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(20), nullable=False)
    eye_color = Column(String(20), nullable=False)
    films = Column(String, nullable=False)
    gender = Column(String(20), nullable=False)
    hair_color = Column(String(20), nullable=False)
    height = Column(Float, nullable=False)
    homeworld = Column(String(20), nullable=False)
    mass = Column(Float, nullable=False)
    name = Column(String(40), nullable=True)
    skin_color = Column(String(20), nullable=False)
    species = Column(String, nullable=False)
    starships = Column(String, nullable=False)
    vehicles = Column(String, nullable=False)


@asynccontextmanager
async def get_session():
    async with async_session_maker() as session:
        async with session.begin():
            yield session
