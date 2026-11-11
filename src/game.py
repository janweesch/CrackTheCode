import random
from src.utils.utils import generate_code
from computer.algorithms import BruteForce
from player.player import HumanPlayer
from player.player import Player
from src.computer.algorithms import AlternatingDigits, SameDigit
from src.utils.utils import get_code, get_mode
class Game:

    class Logger:
        OUTPUT_SPACE = 50
        WIDTH = 50

        def __init__(self, game):
            self.game = game

        def log_table(self, guess: str, match: int):

            print(end="\r")
            print(f"{self.game.get_current_player().who_am_i():{Game.Logger.OUTPUT_SPACE}s}"f"{guess:{Game.Logger.OUTPUT_SPACE}s}"f"{match}")

        def log_victory(self):
            width = Game.Logger.WIDTH
            player = self.game.get_current_player().who_am_i()
            guesses = self.game.get_current_player().get_guess_counter()

            print("*" * width)
            print(f"*{'CONGRATULATIONS!':^{width - 2}}*")
            print(f"*{f'{player} has won after {guesses} guess(es)':^{width - 2}}*")
            print("*" * width)

    def __init__(self, code_length: int=4):

        self._players = ()
        self._current_player = random.randint(1, 1000000) % 2
        self._code_length = code_length
        self.game_mode = None

    def select_game_mode(self) -> None:

        self.game_mode = get_mode(prompt="Playing against Computer[c] or another Player[p]", selection=['c', 'p'])

    @staticmethod
    def create_player() -> HumanPlayer:

        print("Enter your name:", end =" ")
        name = input()

        code = get_code(code_length=4, secret=True, name=name)
        return HumanPlayer(name=name, code=code)

    def create_computer_player(self) -> Player:

        algo = get_mode(prompt="Select the algorithm: \n BruteForce[b]", selection=['b', 'a', 's'])

        match algo:
            case 'b':
                return BruteForce(code=generate_code(code_length=self._code_length))
            case 'a':
                return AlternatingDigits(code=generate_code(code_length=self._code_length))
            case 's':
                return SameDigit(code=generate_code(code_length=self._code_length))

    def set_current_player(self) -> None:
        self._current_player = 1 - self._current_player

    def get_current_player(self) -> Player:
        return self._players[self._current_player]

    def compare_code(self, guess: str) -> int:

        match = 0
        for i, j in zip(guess, self._players[1-self._current_player].get_code()):
            if i==j:
                match+=1

        return match

    def game_loop(self):

        self.select_game_mode()
        self._players = (self.create_player(), self.create_computer_player()) if self.game_mode == "c" else (self.create_player(), self.create_player())

        logger = Game.Logger(self)
        guess = self.get_current_player().next_guess()

        match = self.compare_code(guess=guess)
        logger.log_table(guess=guess, match=match)

        while match < self._code_length:

            self.set_current_player()
            guess = self.get_current_player().next_guess()

            match = self.compare_code(guess=guess)
            logger.log_table(guess=guess, match=match)

        logger.log_victory()

if __name__=="__main__":
    crackthecode = Game()
    crackthecode.game_loop()