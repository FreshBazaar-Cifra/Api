from sqlalchemy import Column, Integer, SmallInteger, String

from models.db_session import SqlAlchemyBase as Base


class Promocode(Base):
    __tablename__ = 'promocodes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale = Column(SmallInteger)
    count = Column(Integer)
    code = Column(String)
