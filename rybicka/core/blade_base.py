from abc import ABC, abstractmethod

class BaseBlade(ABC):
    name = "unnamed"
    description = "no description"
    arg_spec: dict[str, str] = {}

    def __init__(self):
        self.args = {}

    def set_arg(self, key, value):
        if key not in self.arg_spec:
            raise ValueError(f"Argument '{key}' is not defined!")
        self.args[key] = value

    @abstractmethod
    def run(self):
        pass
