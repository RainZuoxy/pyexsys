from enum import Enum


class LogicalInferenceType(Enum):
    INCLUDE = 'include'
    NO_INCLUDE = 'no_include'
    GREATER_THAN = 'gt'
    LESS_THAN = 'lt'
    EQUAL = 'equal'
    NO_EQUAL = 'no_equal'
    SIMILAR = 'similar'
    # NO_SIMILAR = 'no_similar'
    GREATER_OR_EQUAL = 'ge'
    LESS_OR_EQUAL = 'le'
    DEFAULT = 'default'

    @classmethod
    def get_all(cls):
        return [
            LogicalInferenceType.INCLUDE,  LogicalInferenceType.NO_INCLUDE,
            LogicalInferenceType.GREATER_THAN, LogicalInferenceType.LESS_THAN,
            LogicalInferenceType.EQUAL,  LogicalInferenceType.NO_EQUAL,
            LogicalInferenceType.SIMILAR,  # LogicalInferenceType.NO_SIMILAR,
            LogicalInferenceType.GREATER_OR_EQUAL, LogicalInferenceType.LESS_OR_EQUAL,
            LogicalInferenceType.DEFAULT
        ]


class LogicalGateType(Enum):
    AND = 'and'
    OR = 'or'
    NOT = 'not'
