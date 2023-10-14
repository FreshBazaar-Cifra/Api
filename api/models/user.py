from sqlalchemy import Column, Integer, String, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import SqlAlchemyBase as Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    avatar = Column(String)

    @classmethod
    async def get_by_login(cls, login: str, session: AsyncSession):
        """
        Get user by his id

        :param login: login of user
        :param session: session
        :return: User
        :rtype: User
        """

        _ = await session.execute(select(cls).where(cls.login == login))
        return _.scalar()

    @classmethod
    async def get_by_id(cls, user_id: int, session: AsyncSession):
        """
        Get user by his id

        :param user_id: id of user from db
        :param session: session
        :return: User
        :rtype: User
        """

        _ = await session.execute(select(cls).where(cls.id == user_id))
        return _.scalar()

    @classmethod
    async def change_user_names(cls, user_id: int, first_name: str, last_name: str, session: AsyncSession):
        """
        Update user name

        :param user_id: id of user
        :param first_name: new first name of user
        :param last_name: new last name of user
        :param session: session
        :return: None
        """

        await session.execute(update(cls).where(cls.id == user_id).values(first_name=first_name, last_name=last_name))
        await session.commit()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
