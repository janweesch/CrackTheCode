from abc import ABC, abstractmethod
import random

class Algorithm(ABC):

    @abstractmethod
    def next_guess(self) -> str:
        pass

class BruteForce(Algorithm):

    def __init__(self, code_length: int):

        self._code_length = code_length

    def next_guess(self) -> str:
        code = ""
        for i in range(self._code_length):
            code += str(random.randrange(0, 10, 1))
        return code

class SameDigit(Algorithm):

    def __init__(self, code_length: int):

        self._code_length = code_length
        self._guesses = 0

    def next_guess(self) -> str:

        code = "0000"
        if self._guesses < 10:
            code = self._code_length*str(self._guesses)
        self._guesses += 1

        return code

class AlternatingDigits(Algorithm):

    def __init__(self, code_length: int):

        self._code_length = code_length
        self._guesses = 0

    def next_guess(self) -> str:

        code = "0000"
        if self._guesses < 10:
            code = ''.join(f"{(i+self._guesses) % 10}" for i in range(self._code_length))
        self._guesses += 1

        return code

class Backtracking(Algorithm):

    def next_guess(self):
        pass


class MiniMax(Algorithm):
    def next_guess(self) -> str:
        pass


    def max(self):
        pass

    def min(self):
        pass

