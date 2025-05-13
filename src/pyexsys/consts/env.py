import os

PYEXSYS_LOG_PATH = os.environ.get('PYEXSYS_LOG_PATH')

PYEXSYS_DB_TYPE = os.environ.get('PYEXSYS_DB_TYPE','sqlite')  # SQLITE, POSTGRESQL
PYEXSYS_POSTGRESQL_SCHEMA = os.environ.get('PYEXSYS_DB_TYPE','sqlite')  # SQLITE, POSTGRESQL

PYEXSYS_DB_ECHO = True if os.environ.get('PYEXSYS_DB_ECHO', 'OFF').upper() == 'ON' else False
