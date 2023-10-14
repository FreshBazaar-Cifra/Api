from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, SmallInteger, Time, CheckConstraint
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base


class WorkingHour(Base):
    __tablename__ = 'working_hours'

    id = Column(Integer, primary_key=True, autoincrement=True)
    day_of_week = Column(SmallInteger)
    opening_time = Column(Time)
    closing_time = Column(Time)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=True)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=True)
    market = relationship("Market", back_populates="working_hours")
    place = relationship("Place", back_populates="working_hours")

    __table_args__ = (
        CheckConstraint('(market_id IS NOT NULL) OR (place_id IS NOT NULL)',
                        name='check_market_place_ids'),
    )
