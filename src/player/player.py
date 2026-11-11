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

    @abstractmethod
    def get_guess_counter(self) -> int:
        pass

class HumanPlayer(Player):

    def __init__(self, name:str, code:str):

        self._name = name
        self._code = code
        self._guess_counter = 0

    def next_guess(self) -> str:
        self._guess_counter += 1
        return get_code(code_length=len(self._code), name=self._name)

    def get_code(self) -> str:
        return self._code

    def who_am_i(self) -> str:
       return self._name

    def get_guess_counter(self) -> int:
        return self._guess_counter