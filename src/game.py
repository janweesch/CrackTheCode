import math
import random
from computer.brain import generate_code
from computer.brain import ComputerPlayer
from computer.algorithms import BruteForce


class Game:

    class Logger:
        OUTPUT_SPACE = 50
        WIDTH = 50

        def __init__(self, game):
            self.game = game

        def log_table(self, guess: str, match: int):

            print(f"{self.game.get_current_player():{Game.Logger.OUTPUT_SPACE}s} {guess: {Game.Logger.OUTPUT_SPACE}s} {match}")

        def log_victory(self):
            print("*" * Game.Logger.WIDTH)
            print(f"* {'CONGRATULATIONS: ' + self.game.get_current_player():^{Game.Logger.WIDTH - 4}} *")
            print("*" * Game.Logger.WIDTH)

    def __init__(self, code_length: int=4):

        self._players = ()
        self._current_player = random.randint(1, int(math.inf)) % 2
        self._code_length = code_length
        self._allowed_code = set("0123456789")
        self.game_mode = None

    def select_players(self) -> None:

        print( "Playing against computer[c] or player[p]?" )
        print( "Enter: ")
        self.game_mode = input()

        if self.game_mode == 'c':
            print("Enter your Name: ")
            name = input()
            print("Enter your code: ")
            code = input()
            self._players = ((name, code), ("computer", generate_code(code_length=self._code_length)))
            print("Select the algorithms: BruteForce[b]")
            algo = input()
            match algo:
                case 'b':
                    computer = ComputerPlayer(BruteForce(code_length= self._code_length))

        else:
            print("Enter name of Player 1: ")
            name_1 = input()
            print(f"Enter your code {name_1}:")
            code_1 = input()

            print("Enter name of Player 2: ")
            name_2 = input()
            print(f"Enter your code {name_2}:")
            code_2 = input()

            self._players = ((name_1, code_1), (name_2, code_2))

    def set_current_player(self) -> None:
        self._current_player = 1 - self._current_player

    def get_current_player(self) -> str:
        return self._players[self._current_player][0]

    def compare_code(self, guess: str) -> int:

        if len(guess) > self._code_length:
            raise ValueError(f"Your guess is longer than the expected code. Guess Length: {len(guess)} > Expected Code Length: {self._code_length}")

        elif len(guess) < self._code_length:
            raise ValueError(f"Your guess is longer than the expected code. Guess Length: {len(guess)} < Expected Code Length: {self._code_length}")

        match = 0
        for i, j in zip(guess, self._players[self._current_player][1]):
            if i==j:
                match+=1

        return match

    def get_guess(self):

        if self.get_current_player()=="Computer":
            print("Computer is guessing... \r")
            #ToDo
            # return guess
        else:
            print(f"{self.get_current_player()} enter your guess: \r")
            return input()

    def game_loop(self):

        logger = Game.Logger(self)
        guess = self.get_guess()
        match = self.compare_code(guess=guess)
        logger.log_table(guess=guess, match=match)

        while match < self._code_length:

            self.set_current_player()
            guess = self.get_guess()
            logger.log_table(guess=guess, match=match)
            match = self.compare_code(guess=guess)

    def verify_code(self, code:str) -> None:

        verify = all(c in self._allowed_code for c in code)

        if not verify:
            raise ValueError("Your code must contain only integers.")

if __name__=="__main__":
    crackthecode = Game()
    crackthecode.game_loop()