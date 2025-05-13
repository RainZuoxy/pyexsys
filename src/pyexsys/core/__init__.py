from abc import ABC, abstractmethod
from collections import deque
from typing import Any, List, Deque, Set

from dataclasses import dataclass

from pydantic import BaseModel

from pyexsys.core.logic_chain import LogicChainGroupItem, ResultItem, RuleItem
from pyexsys.types.relationship import LogicalInferenceType, LogicalGateType


class BaseKnowledge(ABC):
    ...


class BaseInferenceEngine(ABC):

    @abstractmethod
    def get_specific_attributes(self) -> Set:
        return set()

    def is_subset(self, nodes) -> bool:
        return set(nodes) <= self.get_specific_attributes()

    def filter_groups_by_subset_of_specific_attributes(
            self, group_items: Deque[LogicChainGroupItem]
    ) -> List[LogicChainGroupItem]:
        """
        Filter groups by rule attributes.

        Given a deque of LogicChainGroupItem, this function will filter out the groups whose
        rule attributes are subset of the class variable `SPECIFIC_NODES`.

        Parameters
        ----------
        group_items : deque[LogicChainGroupItem]
            A deque of LogicChainGroupItem.

        Returns
        -------
        List[LogicChainGroupItem]
            A list of LogicChainGroupItem whose rule attributes are subset of the class variable `SPECIFIC_NODES`.
        """
        return [
            item for item in group_items
            if self.is_subset(nodes=item.get_set_by_rule_attributes())
        ]


class BaseInferenceItem(BaseModel):
    parent_id: Any
    group_id: int
    relationship: LogicalInferenceType


if __name__ == '__main__':
    class Test(BaseInferenceEngine):
        def get_specific_attributes(self):
            return {'a', 'a ', 'b'}


    test = Test()
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
        attribute_name="c", value=1, priority=1,
        logical_gate=LogicalGateType.AND, relationship=LogicalInferenceType.INCLUDE
    )
    r4 = RuleItem(
        group_id=3,
        attribute_name="d", value=1, priority=2,
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

    lg1 = LogicChainGroupItem(rule_items=[r1], result_items=[])
    lg2 = LogicChainGroupItem(rule_items=[r2], result_items=[])
    lg3 = LogicChainGroupItem(rule_items=[r1, r2], result_items=[])
    lg4 = LogicChainGroupItem(rule_items=[r3], result_items=[])
    lg5 = LogicChainGroupItem(rule_items=[r4], result_items=[])
    raw = groups = deque([lg1, lg4, lg2, lg3, lg5])
    tmp = test.filter_groups_by_subset_of_specific_attributes(group_items=raw)
    print(raw)
    print(tmp)
