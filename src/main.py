



def game_loop():
    """Game running loop..."""

    pass


def evaluator(guess: str, truth: str) -> int:
    """This function compares the received codes..."""

    correct = 0

    if len(guess) != len(truth):
        raise ValueError(f"Codes have different lengths. Codes must have length {len(guess)}. Your code has length {len(truth)}.")

    for i,j in zip(guess, truth):
        if i == j:
            correct += 1

    return correct






