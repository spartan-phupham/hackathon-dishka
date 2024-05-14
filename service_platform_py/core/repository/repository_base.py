# pylint: skip-file
from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from starlette import status

from service_platform_py.core.base_schema import CoreModel
from service_platform_py.core.errors import KEY_EXISTS
from service_platform_py.db.base_table import BaseTable
from service_platform_py.service.postgres.dependency import get_db_session

EntityType = TypeVar("EntityType", bound=BaseTable)
SchemaType = TypeVar("SchemaType", bound=CoreModel)


class BaseRepository(Generic[EntityType]):
    entity: Type[EntityType]

    def __init__(
        self,
        database: AsyncSession = Depends(get_db_session),
    ):
        self.database = database

    async def create(self, obj_in: SchemaType | dict) -> EntityType:
        try:
            obj_in_data = jsonable_encoder(obj_in)
            obj = self.entity(**obj_in_data)
            self.database.add(obj)
            await self.save(obj)
            return obj
        except IntegrityError:
            await self.database.rollback()
            raise KEY_EXISTS from None

    async def get(self, obj_id: Any) -> Optional[EntityType]:
        obj_db = await self.database.get(self.entity, obj_id)
        if not obj_db:
            self.raise_not_found(obj_id)
        return obj_db

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[EntityType]:
        db_models = await self.database.execute(
            select(self.entity)
            .where(self.entity.deleted_at.is_(None))
            .limit(limit)
            .offset(skip)
            .order_by(self.entity.id),
        )
        return list(db_models.scalars().fetchall())

    async def remove(self, obj_id: Any) -> EntityType:
        obj = await self.database.get(self.entity, obj_id)
        if not obj:
            self.raise_not_found(obj_id)
        await self.update(
            obj_in={
                "deleted_at": func.now(),
            },
            obj_id=obj.id,
        )
        await self.save(obj)
        return obj

    async def update(self, obj_in: SchemaType | dict, obj_id: Any):
        try:
            obj: EntityType = await self.get(obj_id)
            if type(obj_in) == SchemaType:
                for key, value in obj_in.dict(exclude={self.entity.id}).items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
            else:
                for key, value in obj_in.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
            await self.save(obj)
            return obj
        except IntegrityError as e:
            await self.database.rollback()
            self.raise_not_found(str(e))

    async def save(self, obj):
        await self.database.commit()
        await self.database.flush(obj)
        return obj

    async def filter(
        self,
        condition: list[bool],
        options: ExecutableOption = None,
    ) -> List[EntityType]:
        query = (
            select(self.entity)
            .filter(*condition)
            .where(self.entity.deleted_at.is_(None))
            .order_by(self.entity.id)
        )
        if options:
            query = query.options(options)
        db_models = await self.database.execute(
            query,
        )
        return list(db_models.scalars().fetchall())

    async def find(self, condition: list[bool]) -> EntityType:
        db_models = await self.database.execute(
            select(self.entity)
            .filter(*condition)
            .where(self.entity.deleted_at.is_(None)),
        )
        data = db_models.scalars().first()
        if not data:
            self.raise_not_found("not match with condition")
        return data

    async def bulk_create(self, obj_in: List[SchemaType]) -> List[EntityType]:
        try:
            objs = []
            for obj in obj_in:
                obj_model = self.entity(**obj.dict())
                objs.append(obj_model)
            self.database.add_all(objs)
            await self.save(objs)
            return objs
        except Exception as e:
            await self.database.rollback()
            raise e

    def raise_not_found(self, identify: str):
        name_table = self.entity.__tablename__
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object {identify} not found in {name_table} table !",
        )
