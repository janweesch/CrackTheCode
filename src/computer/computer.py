import random
import time
from src.computer.algorithms import Algorithm
from src.player.player import Player

def generate_code(code_length: int) -> str:
    """Generates a random code once at the beginning of the game..."""
    code = ""
    for i in range(code_length):
        code += str(random.randrange(0, 10, 1))
    return code

class ComputerPlayer(Player):
    """The computer player..."""

    def __init__(self, algorithm: Algorithm, code: str):

        self._guesses = None # set of guesses
        self._algorithm = algorithm
        self._code = code

    def next_guess(self) -> str:
        """Calls an inference step of the algorithm"""
        print("Computer is guessing...", end="\r")
        time.sleep(3)
        return self._algorithm.next_guess()

    def get_code(self) -> str:
        return self._code

    def who_am_i(self) -> str:
        return "Computer"







