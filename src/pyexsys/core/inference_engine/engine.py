import re
from typing import List, Callable, Any

import numpy as np
from pandas import DataFrame, Series

from pyexsys.types.relationship import LogicalGateType
from pyexsys.utils.pipe import Pipe


class BaseInferenceEngine:

    @staticmethod
    def __validate_digital(func):
        def wrapper(value, target_number):
            if isinstance(value, str) and not value.isdigit():
                return False

            if isinstance(value, str) and value.isdigit():
                value = float(value)

            return func(value, target_number)

        return wrapper

    # Function for number compare
    @staticmethod
    def __less_than(value: str | int | float, target_number: int | float):

        if isinstance(value, (int, float)) and value < target_number:
            return True

        return False

    @staticmethod
    def __equal(value: str | int | float, target_number: int):

        if isinstance(value, (int, float)) and value == target_number:
            return True

        return False

    @classmethod
    @__validate_digital
    def less_than(cls, value: str | int | float, target_number: int | float):
        return cls.__less_than(value, target_number)

    @classmethod
    @__validate_digital
    def greater_than(cls, value: str | int | float, target_number: int):
        return not (cls.__less_than(value, target_number) or cls.__equal(value, target_number))

    @classmethod
    @__validate_digital
    def greater_or_equal(cls, value: str | int | float, target_number: int):
        return not cls.__less_than(value, target_number)

    @classmethod
    def less_or_equal(cls, value: str | int | float, target_number: int):
        return cls.__less_than(value, target_number) or cls.__equal(value, target_number)

    # Function for string compare
    @classmethod
    # @__validate_digital
    def equal(cls, value: Any, target_value: Any):
        return value == target_value

    @classmethod
    def include(cls, value, pattern) -> bool:
        return bool(re.match(pattern, value))

    @classmethod
    def include_number(cls, value: str, pattern: str, number: int):
        # 执行正则匹配
        matches = re.findall(pattern, value)
        transposed_matches = [[bool(x) for x in group] for group in matches]
        transform_bool = np.any(np.array(transposed_matches), axis=0)

        if sum(transform_bool) >= number:
            return True
        return False


class LogicalGateOperator:

    @staticmethod
    def logical_gate_and(series: Series):
        return series.all()

    @staticmethod
    def logical_gate_or(series: Series):
        return series.any()

    def _logical_gate_operater(self, logical_gate: LogicalGateType, operator):

        match logical_gate:
            case LogicalGateType.AND:
                return operator
            case LogicalGateType.OR:
                return operator
            case LogicalGateType.NOT:
                return not operator
            case _:
                raise ValueError(f"Invalid logical gate: {logical_gate}")

    @staticmethod
    def pre_action() -> List[Callable]:
        return []

    @staticmethod
    def main_action(logic) -> List[Callable]:
        return []

    @staticmethod
    def post_action() -> List[Callable]:
        return []

    def process(self, df: DataFrame):
        pipe = Pipe(value=df)
        pipeline = []
        pipeline.extend(self.pre_action())
        pipeline.extend(self.main_action())
        pipeline.extend(self.post_action())
        for action in pipeline:
            pipe = pipe.pipe(action)

        return pipe.result()
