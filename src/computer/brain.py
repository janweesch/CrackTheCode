from algorithms import Algorithm

class ComputerPlayer:

    """The computer player..."""

    def __init__(self, algorithm: Algorithm):

        self._guesses = None # set of guesses
        self._algorithm = algorithm

    def generate_code(self) -> str:
        """Generates a random code once at the beginning of the game..."""
        pass


    def next_guess(self) -> str:
        """Calls an inference step of the algorithm"""
        pass






