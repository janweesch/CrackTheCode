from abc import ABC, abstractmethod
import random

class Algorithm(ABC):

    @abstractmethod
    def next_guess(self) -> int:
        pass

class BruteForce(Algorithm):

    def __init__(self, code_length: int):

        self.code_length = code_length

    @abstractmethod
    def next_guess(self) -> str:
        code = ""
        for i in range(self.code_length):
            code += str(random.randrange(0, 10, 1))
        return code

class Backtracking(Algorithm):

    def next_guess(self):
        pass