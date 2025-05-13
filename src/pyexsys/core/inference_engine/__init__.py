from typing import Callable, Dict

from pyexsys.types.relationship import LogicalInferenceType


class InferenceTypeRegister:
    __inference_type_registered: Dict[str, Callable] = {}

    @classmethod
    def register(cls,extend_mappings):
        return {
            LogicalInferenceType:BaseInferenceEngine.include,
        }


if __name__ == '__main__':
    import re
    import numpy as np


    def test1():
        text = "orange_01, pear_02, watermelon_03"
        pattern = r"(apple_\d+)|(banana_\d+)|(grape_\d+)"

        matches = re.findall(pattern, text)

        matched_groups_count = sum(1 for match in matches for group in match if group)

        print(matched_groups_count)  # 输出 0，因为没有匹配到任何组


    # 要匹配的字符串
    text = "apple_01, banana_02, grape_03, apple_04"

    # 正则表达式：匹配 "apple_xx", "banana_xx" 和 "grape_xx"
    pattern = r"(apple_\d+)|(banana_\d+)|(grape_\d+)"

    # 执行正则匹配
    matches = re.findall(pattern, text)
    transposed_matches = [[bool(x) for x in group] for group in matches]
    transform_bool = np.any(np.array(transposed_matches), axis=0)

    # 打印结果
    print(any(transform_bool),sum(transform_bool))
