from sqlalchemy import Column, Integer, ForeignKey, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base

baskets_to_positions = Table(
    "baskets_to_positions",
    Base.metadata,
    Column("basket_id", ForeignKey("baskets.id")),
    Column("position_id", ForeignKey("positions.id")),
)


class Basket(Base):
    __tablename__ = 'baskets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    positions = relationship("Position", secondary=baskets_to_positions, lazy="selectin")

    @classmethod
    async def get_by_user(cls, user_id: int, session: AsyncSession):
        """
        Get basket by user_id

        :param user_id: id of user from DB
        :param session: session
        :return: Basket
        :rtype: Basket | None
        """

        _ = await session.execute(select(cls).where(cls.user_id == user_id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
