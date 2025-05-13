import unittest

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from pyexsys.db.base import BaseORM
from pyexsys.db.convert import convert_model_to_schema
from pyexsys.db.models import RuleORM, ResultORM
from pyexsys.db.schema import ResultSchema, RuleSchema
from pyexsys.types.relationship import LogicalInferenceType, LogicalGateType


class TestDBModule(unittest.TestCase):
    test_session_factory = None

    @classmethod
    def setUpClass(cls):
        cls.test_init_db()

    @classmethod
    def test_init_db(cls):
        engine = create_engine(
            'sqlite:///:memory:',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool
        )
        BaseORM.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        cls.test_session_factory = session_factory

    def test_rule_orm(self):
        with self.test_session_factory() as session:
            rule_orm = RuleORM(
                category='1', group_id=1,
                relationship=LogicalInferenceType.EQUAL, attribute='a', keywords='b',
                priority=1, logical_gate=LogicalGateType.AND
            )
            session.add(rule_orm)
            session.commit()

            # 从数据库查询并转换为 Pydantic 模型
            _rule_orm = session.query(RuleORM).first()
        rule_schema = convert_model_to_schema(model=_rule_orm, schema_class=RuleSchema)
        print(rule_schema.model_dump())
        self.assertTrue(isinstance(rule_schema.model_dump(), dict))

    def test_result_orm(self):
        with self.test_session_factory() as session:
            result_orm = [
                ResultORM(category='1', group_id=1, attribute='a', value='1'),
                ResultORM(category='2', group_id=2, attribute='b', value='b'),
                ResultORM(category='3', group_id=3, attribute='c', value='g'),
                ResultORM(category='4', group_id=4, attribute='d', value='h'),
            ]
            for _orm in result_orm:
                session.add(_orm)
            session.commit()

            # 从数据库查询并转换为 Pydantic 模型
            _result_orms = session.query(ResultORM).all()
        for r in _result_orms:
            result_schema = convert_model_to_schema(model=r, schema_class=ResultSchema)
            print(result_schema.model_dump())
            self.assertTrue(isinstance(result_schema.model_dump(), dict))


if __name__ == '__main__':
    unittest.main()

