from sqlalchemy import Column, Integer, ForeignKey, SmallInteger, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base, session_db


class PlaceRating(Base):
    __tablename__ = 'place_ratings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    estimate = Column(SmallInteger, nullable=False)

    @classmethod
    async def get_by_place_id(cls, place_id: int, user_id: int, session: AsyncSession):
        """
        Get rating by place and user

        :param place_id: id of place from db
        :param user_id: id of user from db
        :param session: db session
        :return: rating
        :rtype: PlaceRating
        """

        _ = await session.execute(select(cls).where(cls.place_id == place_id, cls.user_id == user_id))
        return _.scalar()

    @classmethod
    async def get_average_estimate(cls, place_id: int, session: AsyncSession) -> float:
        """
        Getting the average estimate of exact place

        :param place_id: id of place
        :param session: db session
        :return: average estimate
        """

        _ = await session.execute(select(cls.estimate).where(cls.place_id == place_id))
        estimates = _.scalars().all()
        return sum(estimates) / len(estimates) if estimates else None

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
