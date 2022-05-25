import asyncio
import re
from typing import AsyncIterator, List, Union

import aiohttp
from cache import AsyncLRU


class SwApi:

    BASE_URL = "https://swapi.dev/api"
    ID_REGEX = re.compile(r"https://swapi.dev/api/\w+/(\d+)/")

    def __init__(self):

        self.session = aiohttp.ClientSession()

    @AsyncLRU(maxsize=10000)  # кешируем, чтобы не загружать одну и туже ссылку дважды
    async def _load_link(self, link: str):
        async with self.session.get(link) as response:
            return await response.json()

    async def _enrich_field(self, value: Union[str, List[str]]):
        """
        Если поле - ссылка загружает содержимое ссылки и подменяет ссылку
        """

        if isinstance(value, str) and value.startswith(self.BASE_URL):
            return await self._load_link(value)
        elif isinstance(value, list) and len(value) > 0:
            return await asyncio.gather(*[self._load_link(item) for item in value])
        return value

    async def _enrich_entity(self, entity: dict):
        """
        Выкачивает все ссылки, которые есть в сущности

        """

        if "url" in entity:
            entity["id"] = self.ID_REGEX.search(entity.pop("url")).groups()[0]

        values = await asyncio.gather(
            *[self._enrich_field(value) for value in entity.values()]
        )
        return dict(zip(entity.keys(), values))

    async def _get(self, entity: str, entity_id: int = None) -> dict:
        """"Получает сущность"""

        suffix = f"{entity}/{entity_id}" if entity_id is not None else entity
        return await self._load_link(f"{self.BASE_URL}/{suffix}")

    async def _load_from_list(
        self, link: str, enrich: bool = False
    ) -> AsyncIterator[dict]:

        """Рекурсивно выгружает сущности по ссылке"""

        list_data = await self._load_link(link)

        for item in list_data["results"]:
            yield item if not enrich else await self._enrich_entity(item)

        if list_data["next"]:
            async for page in self._load_from_list(list_data["next"], enrich):
                yield page

    async def _load_entity(self, entity: str, enrich: bool) -> AsyncIterator[dict]:
        """Рекурсивно выгружает сущности по ссылке"""

        async for item in self._load_from_list(f"{self.BASE_URL}/{entity}", enrich):
            yield item

    async def people(self, enrich: bool = True) -> AsyncIterator[dict]:
        async for person in self._load_entity("people", enrich):
            yield person

    async def get_planet(self, planet_id: int) -> dict:
        return await self._get("planet", planet_id)

    async def get_film(self, film_id: int) -> dict:
        return await self._get("films", film_id)

    async def get_specie(self, specie_id: int) -> dict:
        return await self._get("species", specie_id)

    async def get_vehicle(self, vehicle_id: int) -> dict:
        return await self._get("vehicles", vehicle_id)

    async def get_starship(self, starships_id: int) -> dict:
        return await self._get("starships", starships_id)

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
