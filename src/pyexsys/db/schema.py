from pyexsys.db.base import BaseDBSchema
from pyexsys.types.relationship import LogicalInferenceType, LogicalGateType


class RuleSchema(BaseDBSchema):
    category: str
    group_id: int
    relationship: LogicalInferenceType
    attribute: str
    keywords: str
    priority: int
    logical_gate: LogicalGateType


class ResultSchema(BaseDBSchema):
    category: str
    group_id: int
    attribute: str
    value: str
    priority: int

