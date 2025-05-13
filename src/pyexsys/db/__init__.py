from pyexsys.consts.env import PYEXSYS_DB_TYPE, PYEXSYS_POSTGRESQL_SCHEMA


def init_table_args() -> dict:
    tmp = {'extend_existing': True}
    if PYEXSYS_DB_TYPE == 'postgresql' and isinstance(PYEXSYS_POSTGRESQL_SCHEMA, str):
        tmp['schema'] = PYEXSYS_POSTGRESQL_SCHEMA
    return tmp


TABLE_ARGS = init_table_args()
