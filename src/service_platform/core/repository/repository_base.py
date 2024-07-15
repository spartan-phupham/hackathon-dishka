# pylint: skip-file
from datetime import datetime
from enum import Enum
from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, null, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from service_platform.core.base_schema import CoreModel
from service_platform.core.errors import KEY_EXISTS
from service_platform.db.base_table import BaseTable
from service_platform.service.postgres.dependency import get_db_session
from service_platform.settings import logger

EntityType = TypeVar("EntityType", bound=BaseTable)
SchemaType = TypeVar("SchemaType", bound=CoreModel)


class BaseRepository(Generic[EntityType]):
    entity: Type[EntityType]

    def __init__(
        self,
        database: AsyncSession = Depends(get_db_session),
    ):
        self.database = database

    async def save(self, obj):
        await self.database.commit()
        await self.database.flush(obj)
        await self.database.refresh(obj)
        return obj

    async def create(self, obj_in: SchemaType | dict) -> EntityType:
        try:
            obj_in_data = jsonable_encoder(obj_in)

            for key, value in obj_in_data.items():
                if (
                    isinstance(value, str)
                    and key in obj_in.__annotations__
                    and (
                        obj_in.__annotations__[key] == datetime
                        or obj_in.__annotations__[key] == datetime | None
                    )
                ):
                    obj_in_data[key] = datetime.fromisoformat(value)
            obj = self.entity(**obj_in_data)
            self.database.add(obj)
            await self.save(obj)
            return obj
        except IntegrityError as e:
            logger.error(e)
            await self.database.rollback()
            raise KEY_EXISTS from None

    async def get(self, obj_id: Any) -> Optional[EntityType]:
        obj_db = await self.database.get(self.entity, obj_id)
        if not obj_db:
            self.raise_not_found(obj_id)
        return obj_db

    async def remove(self, obj_id: Any) -> None:
        await self.update(
            obj_in={
                "deleted_at": func.now(),
            },
            obj_id=obj_id,
        )

    async def bulk_remove(self, objs: List[EntityType]) -> None:
        for obj in objs:
            await self.update(
                obj_in={
                    "deleted_at": func.now(),
                },
                obj_id=obj.id,
            )

    async def update(
        self, obj_in: SchemaType | dict, obj_id: Any, allow_nulls: List[str] = None
    ):
        try:
            if allow_nulls is None:
                allow_nulls = set()

            update_values = {}
            if isinstance(obj_in, dict):
                for key, value in obj_in.items():
                    if value is not None or key in allow_nulls:
                        update_values[key] = value
            else:
                exclude_key = str(self.entity.id)
                for key, value in obj_in.model_dump(exclude={exclude_key}).items():
                    if value is not None or key in allow_nulls:
                        if isinstance(value, Enum):
                            value = value.value
                        update_values[key] = value

            await self.database.execute(
                (
                    update(self.entity)
                    .where(self.entity.id == obj_id)
                    .values(**update_values)
                    .execution_options(synchronize_session="fetch")
                )
            )
            await self.database.commit()
        except IntegrityError as e:
            await self.database.rollback()
            self.raise_not_found(str(e))

    def _build_filter_query(
        self,
        conditions: list[bool],
        joins: list[tuple],
        order_by_columns: list[str],
        order_by_desc: bool,
        options: Any = None,
    ):
        if not order_by_columns:
            order_by_columns = ["id"]

        query = (
            select(self.entity)
            .filter(*conditions)
            .where(self.entity.deleted_at == null())
        )

        for column in order_by_columns:
            order_by = getattr(self.entity, column)
            if order_by_desc:
                order_by = order_by.desc()
            query = query.order_by(order_by)

        if joins:
            for join in joins:
                query = query.join(*join)

        if options is not None:
            query = query.options(options)
        return query

    async def get_multi(
        self,
        conditions: list[bool],
        joins: list[tuple] = None,
        order_by_columns: list[str] = None,
        order_by_desc: bool = False,
        skip: int = None,
        limit: int = None,
        options: Any | None = None,
    ) -> list[EntityType]:
        query = self._build_filter_query(
            conditions=conditions,
            joins=joins,
            order_by_columns=order_by_columns,
            order_by_desc=order_by_desc,
            options=options,
        )
        if skip is not None:
            query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)

        db_models = await self.database.execute(query)
        return list(db_models.scalars().fetchall())

    async def get_first(
        self,
        conditions: list[bool],
        joins: list[tuple] = None,
        order_by_columns: list[str] = None,
        order_by_desc: bool = False,
        options: Any | None = None,
        raise_error_if_not_found: bool = False,
    ) -> EntityType:
        query = self._build_filter_query(
            conditions=conditions,
            joins=joins,
            order_by_columns=order_by_columns,
            order_by_desc=order_by_desc,
            options=options,
        )
        db_models = await self.database.execute(query)
        data = db_models.scalars().first()
        if data is None and raise_error_if_not_found:
            raise self.raise_not_found(self.entity)
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

    def raise_not_found(self, obj_id: Any):
        name_table = self.entity.__tablename__
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Object {obj_id} not found in {name_table} table!",
        )
