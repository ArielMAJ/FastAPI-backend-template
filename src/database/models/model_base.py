from __future__ import annotations

import datetime
from typing import Any, List, Union

from fastapi_async_sqlalchemy import db
from sqlalchemy import DateTime, MetaData, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import ColumnExpressionArgument
from typing_extensions import Self


class ModelBase(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData()
    session: AsyncSession

    id: Mapped[int] = mapped_column(
        nullable=False, primary_key=True, index=True, autoincrement=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC),
        nullable=False,
        onupdate=datetime.datetime.now(datetime.UTC),
    )
    deleted_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    @classmethod
    async def new(cls, **kwargs) -> Self:
        obj: Self = cls(**kwargs)
        await obj.save()
        await db.session.flush()
        await db.session.refresh(obj)
        return obj

    @classmethod
    async def get_all(
        cls, *criterion: ColumnExpressionArgument[bool], **kwargs: Any
    ) -> List[Self]:
        if criterion:
            stmt = select(cls).filter(*criterion)
        else:
            stmt = select(cls).filter_by(**kwargs)
        result = await db.session.execute(stmt)
        objs = result.scalars().all()
        return objs

    @classmethod
    async def get(
        cls, *criterion: ColumnExpressionArgument[bool], **kwargs: Any
    ) -> Self:
        if criterion:
            result = await db.session.execute(select(cls).filter(*criterion))
        else:
            result = await db.session.execute(select(cls).filter_by(**kwargs))
        return result.scalars().first()

    @classmethod
    async def get_by_id(cls, id: int) -> Union[Self, None]:
        return await cls.get(cls.id == id)

    async def save(self) -> None:
        db.session.add(self)

    async def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        await self.save()

    async def delete(self):
        await db.session.delete(self)

    def __repr__(self) -> str:
        attrs = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in attrs.items())
        return f"<{self.__class__.__name__}({attrs_str})>"
