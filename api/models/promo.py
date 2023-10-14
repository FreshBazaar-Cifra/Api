from sqlalchemy import Column, Integer, SmallInteger, String, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base


class Promocode(Base):
    __tablename__ = 'promocodes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale = Column(SmallInteger, nullable=False)
    count = Column(Integer, nullable=False)
    code = Column(String, nullable=False)

    @classmethod
    async def get(cls, code: str, session: AsyncSession):
        """
        Get promocode by code

        :param code: string code of promocode
        :param session: db session
        :return: Promocode
        :rtype: Promocode
        """

        _ = await session.execute(select(cls).where(cls.code == code))
        return _.scalar()

    @classmethod
    async def get_by_id(cls, promo_id, session: AsyncSession):
        """
        Get promocode by code

        :param promo_id: id of promocode
        :param session: db session
        :return: Promocode
        :rtype: Promocode
        """

        _ = await session.execute(select(cls).where(cls.id == promo_id))
        return _.scalar()
