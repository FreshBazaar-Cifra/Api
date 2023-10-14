import datetime

from sqlalchemy import Column, Integer, String, DateTime

from models.db_session import SqlAlchemyBase as Base


class Deliveryman(Base):
    __tablename__ = 'deliverymen'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    reg_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    phone = Column(String, nullable=False)
    city = Column(String, nullable=False)
