from sqlalchemy import Column, Integer, ForeignKey, SmallInteger, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Order
from models.db_session import SqlAlchemyBase as Base


class OrderRating(Base):
    __tablename__ = 'order_ratings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order_estimate = Column(SmallInteger, nullable=False)
    delivery_estimate = Column(SmallInteger, nullable=False)

    @classmethod
    async def get_by_order_id(cls, order_id: int, user_id: int, session: AsyncSession):
        """
        Get rating by product and user

        :param order_id: id of order from db
        :param user_id: id of user from db
        :param session: db session
        :return: rating
        :rtype: OrderRating
        """

        _ = await session.execute(select(cls).join(Order).where(Order.id == cls.order_id, cls.order_id == order_id,
                                                                Order.user_id == user_id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()