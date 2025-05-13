from typing import Any


class Pipe:
    def __init__(self, value: Any):
        self.value = value

    def pipe(self, func):
        self.value = func(self.value)
        return self

    def result(self):
        return self.value
