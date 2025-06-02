from abc import ABC, abstractmethod

class BaseBlade(ABC):
    name = "unnamed"
    description = "no description"

    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        pass
