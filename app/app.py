import asyncio
from typing import AsyncIterator

from aioitertools.more_itertools import chunked
from sqlalchemy.dialects.postgresql import insert
from swapi import SwApi

from config import CHUNK_SIZE
from db import People, get_session
from transform import transform_people


async def get_people() -> AsyncIterator[dict]:
    async with SwApi() as sw_api:
        async for person in sw_api.people():  # выгрузка персонажей
            yield transform_people(person)  # преобразование формата


async def main():
    async with get_session() as session:
        async for people_chunk in chunked(get_people(), CHUNK_SIZE):
            query = insert(People).values(people_chunk)  # подготавливаем инсерт
            query = query.on_conflict_do_update(
                constraint="people_pkey",
                set_={
                    column: getattr(query.excluded, column)
                    for column in people_chunk[0].keys()
                    if column != "id"
                },
            )  # в случае, если id существует, обновляем поля, на случай, если API прислал обновленные данные
            await session.execute(query)


asyncio.run(main())
