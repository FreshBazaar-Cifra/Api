import math

from sqlalchemy import Column, Integer, ForeignKey, SmallInteger, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base, session_db


class ProductRating(Base):
    __tablename__ = 'product_ratings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    estimate = Column(SmallInteger)

    @classmethod
    async def get_average_estimate(cls, product_id: int, session: AsyncSession) -> float:
        _ = await session.execute(select(cls.estimate).where(cls.product_id == product_id))
        estimates = _.scalars().all()
        return sum(estimates) / len(estimates) if estimates else None
