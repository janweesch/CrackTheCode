from __future__ import annotations
from itertools import product, accumulate
import random
from typing import TYPE_CHECKING, Generator, List, Tuple

if TYPE_CHECKING:
    from src.game import Game
from src.player.player import Player

class Algorithm(Player):

    _guess_counter = 0
    _code_domain = [] # final search domain to find the opponents code
    _place_holder_domain = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] # list of placeholders
    _domain = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] # possible solution space

    def __init__(self, code: str, game: Game):

        self._code = code
        self.game = game

    def next_guess(self) -> str:
        pass

    @classmethod
    def get_guess_counter(cls) -> int:
        return cls._guess_counter

    @classmethod
    def increment_guess_counter(cls) -> None:
        Algorithm._guess_counter += 1

    @classmethod
    def add_guess_number(cls, number: str, multiplicator: int) -> None:
        Algorithm._code_domain.extend([number]*multiplicator)

    @classmethod
    def remove_place_holder(cls, number: str) -> None:
        Algorithm._place_holder_domain.remove(number)

    @classmethod
    def remove_domain_number(cls, number: str):
        Algorithm._domain.remove(number)

    def get_code(self) -> str:
        return self._code

    def who_am_i(self) -> str:
        return "Computer"

    def two_numbers_guess(self, current_guess: str, number_1: str, index_1: int, number_2: str, index_2: int) -> str:

            current_guess_list = list(current_guess)
            current_guess_list[index_1] = number_1
            current_guess_list[index_2] = number_2
            return ''.join(current_guess_list)

class RandomCode(Algorithm):

    def __init__(self, code: str, game: Game):

        super().__init__(code=code, game=game)

    def next_guess(self) -> str:

        guess = ""

        for i in range(len(self._code)):
            guess += str(random.randrange(0, 10, 1))

        Algorithm.increment_guess_counter()

        return guess

class BruteForce(Algorithm):

    def __init__(self, code: str, game: Game):

        super().__init__(code=code, game=game)

        self._remaining_guesses = product([str(i) for i in range(len(self._code))], repeat=len(self._code))

    def next_guess(self) -> str:

        guess = self._remaining_guesses.__next__()
        guess = ''.join(guess)

        Algorithm.increment_guess_counter()

        return guess

class AlternatingDigits(Algorithm):

    def __init__(self, code: str, game: Game):

        super().__init__(code=code, game=game)

    def next_guess(self) -> str:

        guess = ''.join(f"{(i+self._guess_counter) % 10}" for i in range(len(self._code)))

        return guess

class Backtracking(Algorithm):

    class SameDigit(Algorithm):

        def next_guess(self) -> str:

            guess_number = random.choice(Algorithm._domain)
            guess = len(self._code) * guess_number
            match = self.game.compare_code(guess=guess)

            Algorithm.add_guess_number(number=guess_number, multiplicator=match)
            Algorithm.remove_domain_number(number=guess_number)
            if match > 0:
                Algorithm.remove_place_holder(number=guess_number)

            return guess

    def __init__(self, code: str, game: Game, pre_algo: Algorithm | None = None):

        super().__init__(code=code, game=game)

        if pre_algo is None:
            pre_algo = self.SameDigit(code=code, game=game)

        self.pre_algo = pre_algo
        self.backtracking = None

    def next_guess(self) -> str:

        if len(Algorithm._code_domain )<len(self._code):
            guess = self.pre_algo.next_guess()
            if self.backtracking is None and len(Algorithm._code_domain) == len(self._code):
                starting_guess = len(self._code) * random.choice(Algorithm._place_holder_domain)
                self.backtracking = self._backtrack(current_guess=starting_guess, index=0, current_domain=Algorithm._code_domain.copy())

        elif self.backtracking is not None:
            guess = next(self.backtracking)

        Algorithm.increment_guess_counter()

        return guess

    def _backtrack(self, current_guess: str, index: int, current_domain: List[str]) -> Generator[str]:

        if len(self._code)-index <= 2:
            yield current_guess[:-2] + current_domain[-2] + current_domain[-1]

            if self.game.compare_code(guess=current_guess) == len(self._code)-2:
                yield current_guess[:-2] + current_domain[-1] + current_domain[-2]

            elif self.game.compare_code(guess=current_guess) == len(self._code):
                return

        for c in current_domain:

            current_guess = current_guess[:index] + c + current_guess[index+1:]
            yield current_guess

            # match
            match = self.game.compare_code(guess=current_guess)
            if match > index:
                current_domain.remove(c)
                yield from self._backtrack(current_guess=current_guess, index=index+1, current_domain=current_domain)

class BinaryBacktracking(Backtracking):

    def next_guess(self):

        if len(Algorithm._code_domain) < len(self._code):
            guess = self.pre_algo.next_guess()
            if self.backtracking is None and len(Algorithm._code_domain) == len(self._code):
                starting_guess = len(self._code) * random.choice(Algorithm._place_holder_domain)
                self.backtracking = self._binary_search(guess=starting_guess, current_domain=Algorithm._code_domain.copy())

        elif self.backtracking is not None:
            guess = next(self.backtracking)

        Algorithm.increment_guess_counter()

        return guess


    def _binary_search(self, guess: str, current_domain: List[str]) -> Generator[str]:

        def generate_prefix_list(guess: str, counting_val: str) -> List[int]:

            guess = list(guess)
            return list(accumulate([1 if elem == counting_val else 0 for elem in guess]))

        def split_prefix_list(prefix_list: List[int], middle_pointer: int, right_pointer: int) -> Tuple[int, int]:

            return prefix_list[middle_pointer], prefix_list[right_pointer-1] - prefix_list[middle_pointer]

        place_holder = guess[0]
        _prefix_list = generate_prefix_list(guess=guess, counting_val=place_holder)
        place_holder_count = _prefix_list[-1]
        current_match = 0
        left_pointer = 0
        right_pointer = len(guess)
        middle_pointer = len(guess) // 2

        for c in current_domain:
            ground_truth_guess = guess
            while place_holder_count > 2:

                guess_list = list(guess)
                for pos in range(left_pointer, middle_pointer):
                    guess_list[pos] = c if guess_list[pos] == place_holder else guess_list[pos]

                guess = ''.join(guess_list)
                yield guess

                _prefix_list = generate_prefix_list(guess=guess, counting_val=place_holder)

                match = self.game.compare_code(guess=guess)

                if match > current_match:
                    left_pointer = middle_pointer
                    middle_pointer = (left_pointer + right_pointer) // 2
                    _, place_holder_count = split_prefix_list(prefix_list=_prefix_list, middle_pointer=middle_pointer,
                                                              right_pointer=right_pointer)

                elif match == current_match:
                    right_pointer = middle_pointer
                    middle_pointer = (left_pointer + right_pointer) // 2
                    place_holder_count, _ = split_prefix_list(prefix_list=_prefix_list, middle_pointer=middle_pointer,
                                                              right_pointer=right_pointer)

                guess = ground_truth_guess

            index_1 = guess[left_pointer:right_pointer].index(place_holder)
            index_2 = (len(guess) - 1 - guess[right_pointer::-1].index(place_holder))

            guess = self.two_numbers_guess(current_guess=guess, number_1=c, index_1=index_1, number_2=place_holder, index_2=index_2)

            yield guess

            match = self.game.compare_code(guess=guess)

            if current_match == match:
                guess = self.two_numbers_guess(current_guess=guess, number_1=c, index_1=index_2, number_2=place_holder, index_2=index_1)

                if len(current_domain)==2:
                    yield guess

            current_match = match

            left_pointer = guess.index(place_holder)
            right_pointer = len(guess) - guess[::-1].index(place_holder)
            middle_pointer = (left_pointer+right_pointer) // 2
            _prefix_list = generate_prefix_list(guess=guess, counting_val=place_holder)
            place_holder_count = _prefix_list[right_pointer-1]
