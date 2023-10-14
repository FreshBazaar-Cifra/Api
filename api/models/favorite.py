from sqlalchemy import Column, Integer, ForeignKey, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base

favorites_to_products = Table(
    "favorites_to_products",
    Base.metadata,
    Column("favorite_id", ForeignKey("favorites.id")),
    Column("product_id", ForeignKey("products.id")),
)


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    products = relationship("Product", secondary=favorites_to_products, lazy="selectin")

    @classmethod
    async def get_by_user(cls, user_id: int, session: AsyncSession):
        """
        Get favorite by user

        :param user_id: id of user
        :param session: session
        :return: Favorite
        :rtype: Favorite
        """
        _ = await session.execute(select(cls).where(cls.user_id == user_id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()