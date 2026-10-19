import random
#from algorithms import Algorithm


def generate_code(code_length: int) -> str:
    """Generates a random code once at the beginning of the game..."""
    code = ""
    for i in range(code_length):
        code += str(random.randrange(0, 10, 1))
    return code

# class ComputerPlayer:
#
#     """The computer player..."""
#
#     def __init__(self, algorithm: Algorithm):
#
#         self._guesses = None # set of guesses
#         self._algorithm = algorithm
#
#     def next_guess(self) -> str:
#         """Calls an inference step of the algorithm"""
#         pass






