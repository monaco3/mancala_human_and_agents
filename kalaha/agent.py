from abc import ABC, abstractmethod



class Agent(ABC):
    @abstractmethod
    def choose(self, game) -> int:
        pass

    @abstractmethod
    def __str__(self):
        pass

