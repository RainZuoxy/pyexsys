from collections import deque
from functools import total_ordering
from typing import List, Any, Union, Optional, Iterable, Deque, Set
from pydantic import BaseModel, Field, field_validator, model_validator

from pyexsys.types.relationship import LogicalInferenceType, LogicalGateType

"""
RuleItem and ResultItem extends BaseItem

LogicChainGroupItem stores two lists about RuleItem and ResultItem as a group and group id.
When creating this class in initialization process, it will verify whether these group ids are same and sort two lists.

"""


@total_ordering
class BaseItem(BaseModel):
    group_id: int
    priority: int
    ignore_priority: bool = False

    def __eq__(self, other):
        if not issubclass(self.__class__, other.__class__):
            raise ValueError(f'Cannot compare {self.__class__.__name__} with {other.__class__.__name__}')

        if self.ignore_priority:
            return self.group_id == other.group_id
        return self.group_id == other.group_id and self.priority == other.priority

    def __lt__(self, other):
        if not issubclass(self.__class__, other.__class__):
            raise ValueError(f'Cannot compare {self.__class__.__name__} with {other.__class__.__name__}')

        if self.ignore_priority:
            return self.group_id == other.group_id
        return (
                self.group_id < other.group_id or
                self.group_id == other.group_id and self.priority < other.priority
        )


class RuleItem(BaseItem):
    attribute: str
    relationship: LogicalInferenceType
    keywords: Any
    logical_gate: LogicalGateType


class ResultItem(BaseItem):
    attribute: str
    value: Any
    ignore_priority: bool = True


@total_ordering
class LogicChainGroupItem(BaseModel):
    rule_items: List[RuleItem]
    result_items: List[ResultItem]
    group_id: int = None

    @model_validator(mode='after')
    def set_group_id(cls, model):
        unique_group_ids = set([item.group_id for item in (model.rule_items + model.result_items)])
        if len(unique_group_ids) == 1:
            model.group_id = min(unique_group_ids)
            model.sorted_items()
            return model
        raise ValueError('Group id must be unique')

    def sorted_items(self):
        self.rule_items = sorted(self.rule_items)
        self.result_items = sorted(self.result_items)

    def get_set_by_rule_attributes(self) -> Set[Any]:
        return set([item.attribute for item in self.rule_items])

    def get_set_by_result_attributes(self) -> Iterable[str]:
        return set([item.attribute for item in self.result_items])

    def __eq__(self, other):
        return self.group_id == other.group_id

    def __lt__(self, other):
        return self.group_id < other.group_id

    # todo
    # get generate attributes


class LogicChain(BaseModel):
    """"
    FIFO
    """
    items: Deque[LogicChainGroupItem] = Field(default=deque())

    def init_chain(self):
        self.items = deque()

    def clean_chain(self):
        self.items = deque()

    def get_chain_group_ids(self) -> list:
        return [item.group_id for item in self.items]

    def get_chain_result_ids(self) -> list:
        return [group.group_id for group in self.rules]

    def __lshift__(self, other):
        self.rules.append(other)
        return self

    def __rshift__(self, other):
        self.rules.popleft()
        self.rules.append(other)
        return self


class LogicChainManager:

    def __init__(self):
        """
        Initialize LogicChainManager object.

        `LogicChainManager` is a class to manage rule groups and record the count of each group id.

        :ivar logic_chain: A `LogicChain` object. It is FIFO.
        :ivar _group_id_recorder: A dictionary to record count of each group id.
        """
        self.logic_chain = LogicChain()
        self._group_id_recorder = {}
        self.error_recorder = {}
        # todo
        # default attributes
        # exclude attributes

    def save_rules_by_group(self, sorted_rule_groups: List[LogicChainGroupItem]):
        """

        :param sorted_rule_groups:
        :return:
        """

        # Validate
        if not all([isinstance(group, LogicChainGroupItem) for group in sorted_rule_groups]):
            raise TypeError('sorted_rule_groups must be a list of LogicChainGroupItem')

        sorted_rule_groups = sorted(sorted_rule_groups)

        count = 1
        marked_group_id = None
        for group in sorted_rule_groups:
            try:

                self.logic_chain << group

                # First loop
                if marked_group_id is None:
                    marked_group_id = group.group_id
                    continue

                # If current group id is not equal to marked group id
                if marked_group_id in self._group_id_recorder:
                    self.error_recorder = {
                        'error_type': 'group_id_duplicated',
                        'message': f'Group id: {marked_group_id} is not unique'
                    }
                    raise KeyError(f'Group id: {marked_group_id} is not unique')

                # If current group id is equal to marked group id
                if group.group_id == marked_group_id:
                    count += 1
                    continue

                self._group_id_recorder[marked_group_id] = count
                marked_group_id = group.group_id
                count = 1
            except KeyError:
                ...

    def save_results(self, result_items: List[ResultItem]):
        for result_item in result_items:
            self.logic_chain >> result_item


if __name__ == '__main__':
    lc = LogicChain()
    r1 = RuleItem(
        group_id=1,
        attribute_name="a", value=1, priority=3,
        logical_gate=LogicalGateType.AND, relationship=LogicalInferenceType.EQUAL
    )
    r2 = RuleItem(
        group_id=1,
        attribute_name="b", value=1, priority=4,
        logical_gate=LogicalGateType.AND, relationship=LogicalInferenceType.INCLUDE
    )
    r3 = RuleItem(
        group_id=2,
        attribute_name="b", value=1, priority=1,
        logical_gate=LogicalGateType.AND, relationship=LogicalInferenceType.INCLUDE
    )
    r4 = RuleItem(
        group_id=3,
        attribute_name="b", value=1, priority=2,
        logical_gate=LogicalGateType.AND, relationship=LogicalInferenceType.INCLUDE
    )

    re1 = ResultItem(
        group_id=1,
        attribute_name="b", value=1,
        priority=1
    )
    re2 = ResultItem(
        group_id=1,
        attribute_name="b", value=1,
        priority=1
    )
    print(r1 < r2)
    lg1 = LogicChainGroupItem(rule_items=[r1, r2], result_items=[re1, re2])
    r_lst = [r4, r2, r3, r1]
    print(sorted(r_lst))
    # lg2 = LogicChainGroupItem(rule_items=[r1, r3], result_items=[re1, re2])
    print(lg1.group_id)
    # print(lcg1 < lcg4)
    # LogicChainManager().save_rules_by_group(
    #     sorted_rule_groups=[lcg1, lcg2]
    # )
    # print(lc)
