from __future__ import annotations
from itertools import product, accumulate
import random
from typing import TYPE_CHECKING, Generator, List, Tuple, Dict

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

    def two_numbers_guess(self, current_guess_list: List[str], number_1: str, index_1: int, number_2: str, index_2: int) -> str:

        current_guess_list[index_1] = number_1
        current_guess_list[index_2] = number_2
        return ''.join(current_guess_list)

    def fill_missing_number(self, current_guess_list: List[str], number: str, place_holder_list: List[int]) -> str:

        for index in place_holder_list:
            current_guess_list[index] = number

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
                self.backtracking = self._binary_search(guess=starting_guess, search_domain=Algorithm._code_domain.copy())

        elif self.backtracking is not None:
            guess = next(self.backtracking)

        Algorithm.increment_guess_counter()

        return guess

    def _binary_search(self, guess: str, search_domain: List[str]):

        search_domain_map = {code_number: search_domain.count(code_number) for code_number in search_domain}
        search_domain.sort()
        remaining_numbers = search_domain.copy()

        p_h_index_list = [index for index in range(len(guess))] # indexes of place holders (p_h)

        # pointers
        l_p = 0
        r_p = len(guess) # always showing to last element in searching area
        m_p = r_p // 2  # up rounded middle element

        guess_list = list(guess) # guess list

        match = 0 # number of correct positions

        for number in search_domain:

            if  len(set(remaining_numbers)) == 1:
                current_guess = self.fill_missing_number(current_guess_list=guess_list, number=search_domain[0], place_holder_list=p_h_index_list)

                yield current_guess

                return

            elif len(p_h_index_list) == 2:

                # Last possible choices
                current_guess = self.two_numbers_guess(current_guess_list=guess_list, number_1=search_domain[-2],
                                                       index_1=p_h_index_list[0], number_2=search_domain[-1],
                                                       index_2=p_h_index_list[1])

                yield current_guess

                current_match = self.game.compare_code(guess=current_guess)

                if current_match == match:
                    current_guess = self.two_numbers_guess(current_guess_list=guess_list, number_1=search_domain[-2],
                                                           index_1=p_h_index_list[1], number_2=search_domain[-1],
                                                           index_2=p_h_index_list[0])

                    yield current_guess

                    return

            else:
                while True:

                    current_guess_list = guess_list.copy()

                    for index in p_h_index_list[l_p:m_p]:
                        current_guess_list[index] = number

                    current_guess = ''.join(current_guess_list)

                    yield current_guess

                    current_match = self.game.compare_code(guess=current_guess)

                    if current_match == match + m_p - l_p:
                        match += m_p - l_p
                        break

                    # search right
                    elif current_match == match:
                        l_p = m_p
                        m_p = (l_p + r_p) // 2

                    # search left
                    elif current_match > match:
                        r_p = m_p
                        m_p = (l_p + r_p) // 2

                    if l_p == r_p-1:
                        match += r_p - l_p
                        break

                # update guess
                for index in p_h_index_list[l_p:m_p]:
                    guess_list[index] = number

                # update p_h_list
                del p_h_index_list[l_p:m_p]

                # update remaining_numbers
                remaining_numbers.pop(0)

                # update pointer
                l_p = 0
                r_p = len(p_h_index_list)
                m_p = r_p // 2