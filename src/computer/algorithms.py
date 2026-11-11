from itertools import product
import random
from src.player.player import Player

class Algorithm(Player):

    def __init__(self, code: str):

        self._guesses = None # set of guesses
        self._guess_counter = 0
        self._code = code
        self._remaining_codes = product([str(i) for i in range(len(self._code))], repeat=len(self._code))

    def next_guess(self) -> str:
        pass

    def get_guess_counter(self) -> int:
        return self._guess_counter

    def get_code(self) -> str:
        return self._code

    def who_am_i(self) -> str:
        return "Computer"

class RandomCode(Algorithm):

    def __init__(self, code: str):

        super().__init__(code=code)

    def next_guess(self) -> str:

        code = ""
        for i in range(len(code)):
            code += str(random.randrange(0, 10, 1))

        self._guess_counter += 1

        return code

class BruteForce(Algorithm):

    def __init__(self, code: str):

        super().__init__(code=code)

    def next_guess(self) -> str:

        guess = self._remaining_codes.__next__()
        code = ''.join(guess)

        return code

class SameDigit(Algorithm):

    def __init__(self, code: str):

        super().__init__(code=code)

    def next_guess(self) -> str:

        code = "0000"
        if self._guess_counter < 10:
            code = len(code)*str(self._guess_counter)

        self._guess_counter += 1

        return code

class AlternatingDigits(Algorithm):

    def __init__(self, code: str):

        super().__init__(code=code)

    def next_guess(self) -> str:

        code = "0000"
        if self._guess_counter < 10:
            code = ''.join(f"{(i+self._guess_counter) % 10}" for i in range(len(self._code)))

        self._guess_counter += 1

        return code



class Backtracking(Algorithm):

    def __init__(self, code: str):

        super().__init__(code=code)


    def next_guess(self) -> str:
        pass