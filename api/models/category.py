from sqlalchemy import Column, Integer, String

from models.db_session import SqlAlchemyBase as Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
