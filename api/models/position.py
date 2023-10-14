from sqlalchemy import Column, Integer, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base


class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product", lazy="selectin")
    count = Column(Integer, default=1, nullable=False)

    @classmethod
    async def get_position_by_id(cls, position_id: int, session: AsyncSession):
        """
        Get position by its id

        :param position_id: id of position from DB
        :param session: db session
        :return: Position
        :rtype: Position | None
        """

        _ = await session.execute(select(cls).where(cls.id == position_id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()