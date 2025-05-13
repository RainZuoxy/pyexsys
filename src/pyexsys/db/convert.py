from typing import Type

from pyexsys.db.base import BaseORM, BaseDBSchema


def convert_model_to_schema(model: BaseORM, schema_class: Type[BaseDBSchema]) -> BaseDBSchema:
    user_schema = schema_class.model_validate(model)
    return user_schema
