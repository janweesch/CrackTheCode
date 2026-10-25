class Player:

    def __init__(self, code=str):

        self._code = code

    def get_code(self):
        return self._code

    @staticmethod
    def who_am_i():
        print("Player")