from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base


class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True, autoincrement=True)
    logo = Column(String)
    name = Column(String)
    description = Column(String)
    location_photo = Column(String)
    market_id = Column(Integer, ForeignKey("markets.id"))
    market = relationship("Market")
    phones = Column(ARRAY(String))
    working_hours = relationship("WorkingHour", back_populates="place", lazy="selectin")

    @classmethod
    async def get_all_by_market(cls, market_id: int, page: int, limit: int, session: AsyncSession):
        """
        Get all places by market id

        :param market_id: id of market
        :param page: page
        :param limit: limit
        :param session: session
        :return: list of places
        :rtype: list[Place]
        """

        _ = await session.execute(select(cls).where(cls.market_id == market_id).limit(limit).offset(page * limit))
        return _.scalars().all()

    @classmethod
    async def get_by_place_id(cls, place_id: int, session: AsyncSession):
        """
        Get place by its id

        :param place_id: id of place
        :param session: session
        :return: Place
        :rtype: Place
        """

        _ = await session.execute(select(cls).where(cls.id == place_id))
        return _.scalar()
