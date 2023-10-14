from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, ARRAY, Numeric, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from models.db_session import SqlAlchemyBase as Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(Integer, ForeignKey("places.id"))
    place = relationship("Place", lazy="selectin")
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", lazy="selectin")
    description = Column(String)
    images = Column(ARRAY(String), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    weight = Column(Integer, nullable=False)
    manufacturer = Column(String)
    attributes = relationship("Attribute", lazy="selectin")

    @classmethod
    async def get_product_by_id(cls, product_id: int, session: AsyncSession):
        """
        Get product by id

        :param product_id: product id
        :param session: session
        :return: Product
        :rtype: Product
        """

        _ = await session.execute(select(cls).where(cls.id == product_id))
        return _.scalar()

    @classmethod
    async def get_all_by_place_id(cls, place_id: int, page: int, limit: int, session: AsyncSession):
        """
        Get all products by place id

        :param place_id: id of place
        :param page: page
        :param limit: limit
        :param session: session
        :return: list of products
        :rtype: list[Product]
        """

        _ = await session.execute(select(cls).where(cls.place_id == place_id).limit(limit).offset(page * limit))
        return _.scalars().all()

    @classmethod
    async def get_by_ids(cls, product_ids: list[int], session: AsyncSession):
        """
        Get products by its ids

        :param product_ids: ids of products
        :param session: db session
        :return: list of products
        :rtype: list[Product]
        """

        _ = await session.execute(select(cls).where(cls.id.in_(product_ids)))
        return _.scalars().all()

    @classmethod
    async def get(cls, product_id: int, session: AsyncSession):
        """
        Get product by id

        :param product_id: id of product
        :param session: db session
        :return: Product
        :rtype: Product
        """

        _ = await session.execute(select(cls).where(cls.id == product_id))
        return _.scalar()


class Attribute(Base):
    __tablename__ = 'attributes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    value = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

