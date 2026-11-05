from abc import ABC, abstractmethod
from src.utils.utils import get_code

class Player(ABC):

    @abstractmethod
    def next_guess(self) -> str:
        pass

    @abstractmethod
    def get_code(self) -> str:
        pass

    @abstractmethod
    def who_am_i(self) -> str:
        pass

class HumanPlayer(Player):

    def __init__(self, name:str, code:str):

        self.name = name
        self._code = code

    def next_guess(self) -> str:
        return get_code(code_length=len(self._code))

    def get_code(self) -> str:
        return self._code

    def who_am_i(self) -> str:
       return self.name