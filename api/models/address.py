from sqlalchemy import Column, String, Integer, select, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, nullable=False, primary_key=True)
    city = Column(String, nullable=False)
    district = Column(String)
    street = Column(String, nullable=False)
    home = Column(String, nullable=False)
    entrance = Column(String)
    apartment = Column(String)
    intercom = Column(String)
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)

    async def save(self, session: AsyncSession):
        cls = Address
        _ = await session.execute(select(cls).where(cls.city == self.city, cls.district == self.district,
                                                    cls.street == self.street, cls.home == self.home,
                                                    cls.entrance == self.entrance,
                                                    cls.apartment == self.apartment, cls.intercom == self.intercom))
        if address := _.scalar():
            return address.id

        session.add(self)
        await session.commit()
        return self.id

