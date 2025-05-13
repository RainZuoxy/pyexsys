from sqlalchemy import Column, Integer, String, Enum

from pyexsys.db.base import BaseORM
from pyexsys.types.relationship import LogicalGateType, LogicalInferenceType
from pyexsys.db import TABLE_ARGS


class RuleORM(BaseORM):
    __tablename__ = "rules"
    __table_args__ = TABLE_ARGS

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column('category', String, nullable=False)
    group_id = Column('group_id', Integer, nullable=False)
    relationship = Column(
        'relationship',
        Enum(
            LogicalInferenceType, values_callable=lambda x: [e.value for e in x], schema='test'
        ),
        nullable=False
    )
    attribute = Column('attribute', String)
    keywords = Column('keywords', String)
    priority = Column('priority', Integer, nullable=False)
    logical_gate = Column(
        'logical_gate', Enum(LogicalGateType, values_callable=lambda x: [e.value for e in x], schema='test')
    )


class ResultORM(BaseORM):
    __tablename__ = "results"
    __table_args__ = TABLE_ARGS

    category = Column('category', String, primary_key=True, nullable=False)
    group_id = Column('group_id', Integer, primary_key=True, nullable=False)
    attribute = Column('attribute', String)
    value = Column('value', String)
    priority = Column('priority', Integer, primary_key=True, nullable=False)
