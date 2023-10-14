import datetime

from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, select, Table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base


orders_to_positions = Table(
    "orders_to_positions",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("position_id", ForeignKey("positions.id")),
)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", lazy="selectin")
    positions = relationship("Position", secondary=orders_to_positions, lazy="selectin")
    date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    status = Column(String, default="created", nullable=False)
    deliveryman_id = Column(Integer, ForeignKey("deliverymen.id"))
    deliveryman = relationship("Deliveryman", lazy="selectin")
    price = Column(Numeric(10, 2), nullable=False)
    delivery_price = Column(Numeric(7, 2), nullable=False)
    promocode_id = Column(Integer, ForeignKey("promocodes.id"))
    promocode = relationship("Promocode", lazy="selectin")
    total = Column(Numeric(11, 2), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    address = relationship("Address", lazy="selectin")
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)
    market = relationship("Market", lazy="selectin")

    @classmethod
    async def get_orders_by_user(cls, user_id: int, session: AsyncSession):
        """
        Get all orders of user

        :param user_id: id of user
        :param session: session
        :return: list of orders
        :rtype: list[Order]
        """

        _ = await session.execute(select(cls).where(cls.user_id == user_id))
        return _.scalars().all()

    @classmethod
    async def get_order_by_id(cls, order_id: int, user_id: int, session: AsyncSession):
        """
        Get order by id

        :param order_id: id of order
        :param user_id: id of user
        :param session: session
        :return: Order
        :rtype: Order
        """

        _ = await session.execute(select(cls).where(cls.id == order_id, cls.user_id == user_id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
