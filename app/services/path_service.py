from typing import Annotated
from uuid import UUID

import httpx
from fastapi import Depends

from app.core.settings import settings
from app.exceptions.erros import NotFoundError
from app.repositories.path_repository import PathRepository
from app.schemas.filters_params_schema import SortEnum
from app.schemas.path_schema import PathCreate, PathResponse, PathResponseList


class PathService:
    def __init__(
        self,
        repository: Annotated[PathRepository, Depends()],
    ) -> None:
        self.repository = repository

    async def get_all_paths(
        self,
        skip: int,
        limit: int,
        order_by: str,
        arranging: SortEnum,
    ) -> PathResponseList:
        db_paths = await self.repository.search_all(
            skip, limit, order_by, arranging
        )
        return PathResponseList(
            data=[PathResponse.model_validate(path) for path in db_paths]
        )

    async def get_path_by_id(self, path_id: UUID) -> PathResponse:
        db_path = await self.repository.search(path_id)
        if db_path is None:
            raise NotFoundError
        return PathResponse.model_validate(db_path)

    async def create_path(self, path: PathCreate) -> PathResponse:
        base_url = settings.OSRM_URL + 'table/v1/driving/'
        coords = [f'{path.pickup.lng},{path.pickup.lat}']
        coords.extend(f'{coord.lng},{coord.lat}' for coord in path.dropoff)
        coords_url = ';'.join(coords)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f'{base_url}{coords_url}',
                params={'annotations': 'duration,distance'},
            )
            response.raise_for_status()
        db_path = await self.repository.create(path.model_dump())
        return PathResponse.model_validate(db_path)

    async def delete_path(self, path_id: UUID) -> None:
        path = await self.repository.search(path_id)
        if path is None:
            raise NotFoundError
        return await self.repository.delete(path)
