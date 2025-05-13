from typing import Type

from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session


class BaseORM(DeclarativeBase):
    pass


class BaseDBSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseDBCreator:
    db_engine = None
    session_factory = None
    scoped_session = None

    @staticmethod
    def get_baseorm() -> Type[BaseORM]:
        return BaseORM

    @classmethod
    def init(cls, db_url: str):
        if cls.db_engine is None:
            cls.db_engine = create_engine(url=db_url, echo=True)

        if cls.scoped_session is None:
            cls.session_factory = sessionmaker(bind=cls.db_engine, autoflush=False, autocommit=False)
        if cls.scoped_session is None:
            cls.scoped_session = scoped_session(cls.session_factory)

    @classmethod
    def get_session(cls):
        """获取数据库会话"""
        return cls.scoped_session()

    @classmethod
    def init_db(cls):
        """初始化数据库（创建所有表）"""
        cls.get_baseorm().metadata.create_all(bind=cls.db_engine)

    @classmethod
    def drop_db(cls):
        """删除所有表"""
        cls.get_baseorm().metadata.drop_all(bind=cls.db_engine)

    @classmethod
    def close(cls):
        """关闭 session 和引擎"""
        cls.scoped_session.remove()
        cls.db_engine.dispose()
