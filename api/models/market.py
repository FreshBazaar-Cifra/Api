from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, Numeric, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base


class Market(Base):
    __tablename__ = 'markets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    images = Column(ARRAY(String))
    city = Column(String)
    street = Column(String)
    district = Column(String)
    house = Column(String)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    working_hours = relationship("WorkingHour", back_populates="market", lazy="selectin")

    @classmethod
    async def get_all(cls, page: int, limit: int, session: AsyncSession):
        """
        Get all markets

        :param page: page
        :param limit: limit
        :param session: session
        :return: list of markets
        :rtype: list[Market]
        """

        _ = await session.execute(select(cls).limit(limit).offset(page * limit))
        return _.scalars().all()

    @classmethod
    async def get_by_market_id(cls, market_id: int, session: AsyncSession):
        """
        Get market by its id

        :param market_id: id of place
        :param session: session
        :return: Market
        :rtype: Market
        """

        _ = await session.execute(select(cls).where(cls.id == market_id))
        return _.scalar()
