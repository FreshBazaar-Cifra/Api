from sqlalchemy import Column, Integer, ForeignKey, SmallInteger

from models.db_session import SqlAlchemyBase as Base


class OrderRating(Base):
    __tablename__ = 'order_ratings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order_estimate = Column(SmallInteger)
    delivery_estimate = Column(SmallInteger)
