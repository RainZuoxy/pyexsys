from typing import List

from pyexsys.db.base import BaseDBCreator

from pyexsys.db.models import RuleORM, ResultORM

from pyexsys.logging import pyexsys_logger as logger


class BaseKnowledgeDB:

    @classmethod
    def filter_rules_by_category(cls, category: str):
        logger.debug(msg=f'Filter rules by category: {category}')
        with BaseDBCreator.scoped_session() as session:
            return (
                session.query(RuleORM)
                .filter_by(category=category)
                .order_by(RuleORM.group_id, RuleORM.priority)
                .all()
            )

    @classmethod
    def test(cls, category: str, specific_attributes: set):
        with BaseDBCreator.scoped_session() as session:
            return (
                session.query(RuleORM.group_id).filter(
                    RuleORM.category == category,
                    RuleORM.attribute.in_(specific_attributes)
                )
                .distinct().all()
            )

    @classmethod
    def filter_rules_by_category_and_logical_gate(cls, category: str = None, logical_gate: str = None):
        logger.debug(msg=f'Filter rules by category: {category} and logical gate: {logical_gate}')
        with BaseDBCreator.scoped_session() as session:
            query = session.query(RuleORM)
            if category is not None:
                query = query.filter_by(category=category)
            if logical_gate is not None:
                query = query.filter_by(logical_gate=logical_gate)
            return query.order_by(RuleORM.group_id, RuleORM.priority).all()

    @classmethod
    def filter_rules_by_category_and_group_id(cls, category: str = None, group_id: int = None):
        logger.debug(msg=f"Filter rules by category: {category} and group_id: {group_id}")
        with BaseDBCreator.scoped_session() as session:
            query = session.query(RuleORM)
            if category is not None:
                query = query.filter_by(category=category)
            if group_id is not None:
                query = query.filter_by(group_id=group_id)
            return query.order_by(RuleORM.group_id, RuleORM.priority).all()

    @classmethod
    def filter_rules_by_category_and_group_ids(cls, category: str = None, group_ids: List[int] = None):
        logger.debug(msg=f"Filter rules by category: {category} and group_ids: {group_ids}")
        with BaseDBCreator.scoped_session() as session:
            query = session.query(RuleORM)
            if category is not None:
                query = query.filter_by(category=category)
            if group_ids:
                query = query.filter(RuleORM.group_id.in_(group_ids))
            return query.order_by(RuleORM.group_id, RuleORM.priority).all()

    @classmethod
    def filter_results_by_category(cls, category):
        logger.debug(msg=f"Filter results by category: {category}")
        with BaseDBCreator.scoped_session() as session:
            query = session.query(ResultORM)
            query = query.filter_by(category=category)
            return query.order_by(ResultORM.group_id, ResultORM.priority).all()

    @classmethod
    def add_rules(cls, rules: List[RuleORM]):
        with BaseDBCreator.scoped_session() as session:
            _before = session.query(RuleORM).count()
            session.add_all(rules)
            session.commit()
            _after = session.query(RuleORM).count()
            return _after - _before

    @classmethod
    def add_results(cls, results: List[ResultORM]):
        with BaseDBCreator.scoped_session() as session:
            _before = session.query(ResultORM).count()
            session.add_all(results)
            session.commit()
            _after = session.query(ResultORM).count()
            return _after - _before


if __name__ == '__main__':

    def add_rules():
        import pandas as pd
        # BaseDBCreator.init(db_url='sqlite:///./test.db')
        BaseDBCreator.init(db_url='postgresql://test_user:test12345@192.168.71.16:3003/testdb')
        BaseDBCreator.init_db()
        rules_df = pd.read_csv(r"D:\pythonproject\Auto_Coding_Tool\Database\Rules.csv")
        print(rules_df.shape)
        input_rules = []
        for index, row in rules_df.iterrows():
            input_rules.append(RuleORM(
                category=row['CATG_NO'],
                group_id=row['COND_GROUP'],
                relationship=row['COND_RELATIONSHIP'],
                attribute=row['COND_ATTRIBUTE'],
                keywords=row['COND_KEYWORD'],
                priority=row['COND_PRIORITY'],
                logical_gate=row['COND_LOGIC_GATE']
            ))
        rule_count = BaseKnowledgeDB.add_rules(input_rules)
        print(rule_count)


    def add_results():
        import pandas as pd
        # BaseDBCreator.init(db_url='sqlite:///./test.db')
        BaseDBCreator.init(db_url='postgresql://test_user:test12345@192.168.71.16:3003/testdb')
        BaseDBCreator.init_db()
        rules_df = pd.read_csv(r"D:\pythonproject\Auto_Coding_Tool\Database\Results.csv")
        print(rules_df.shape)
        input_results = []
        for index, row in rules_df.iterrows():
            input_results.append(ResultORM(
                category=row['CATG_NO'],
                group_id=row['COND_GROUP'],
                attribute=row['CONS_ATTRIBUTE'],
                value=row['CONS_KEYWORD'],
                priority=row['CONS_PRIORITY'],
            ))
        result_count = BaseKnowledgeDB.add_results(input_results)
        print(result_count)


    # add_rules()
    # BaseDBCreator.init(db_url='sqlite:///./test.db')
    def test_query():
        from pyexsys.db.schema import RuleSchema
        from pyexsys.db.convert import convert_model_to_schema
        BaseDBCreator.init(db_url='postgresql://test_user:test12345@192.168.71.16:3003/testdb')
        BaseDBCreator.init_db()
        rule_count = BaseKnowledgeDB.filter_rules_by_category(category='709')
        print(len(rule_count))
        # print(result_count)
        rule_schema = [convert_model_to_schema(model=_rule, schema_class=RuleSchema).model_dump() for _rule in
                       rule_count]
        print(rule_schema)


    add_results()
    # import sqlite3
    #
    # conn = sqlite3.connect('./test.db')
    # cursor = conn.cursor()
    #
    # cursor.execute("SELECT * FROM rules where category = '709'")
    # rows = cursor.fetchall()
    #
    # for row in rows:
    #     print(row)
    #
    # conn.close()
