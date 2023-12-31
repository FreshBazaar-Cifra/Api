from sqlalchemy import Column, Integer, ForeignKey, SmallInteger, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base, session_db


class ProductRating(Base):
    __tablename__ = 'product_ratings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    estimate = Column(SmallInteger, nullable=False)

    @classmethod
    async def get_by_product_id(cls, product_id: int, user_id: int, session: AsyncSession):
        """
        Get rating by product and user

        :param product_id: id of product from db
        :param user_id: id of user from db
        :param session: db session
        :return: rating
        :rtype: ProductRating
        """

        _ = await session.execute(select(cls).where(cls.product_id == product_id, cls.user_id == user_id))
        return _.scalar()

    @classmethod
    async def get_average_estimate(cls, product_id: int, session: AsyncSession) -> float:
        """
        Getting the average estimate of exact product

        :param product_id: id of product
        :param session: db session
        :return: average estimate
        """

        _ = await session.execute(select(cls.estimate).where(cls.product_id == product_id))
        estimates = _.scalars().all()
        return sum(estimates) / len(estimates) if estimates else None

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
