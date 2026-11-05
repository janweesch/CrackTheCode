import sys
from typing import List

def get_code(code_length: int, prompt: str = "Enter your Code:", secret: bool = False) -> str:
    code = ""

    print(prompt, end=" ", flush=True)


    if sys.platform == "win32":
        import msvcrt

        def read_char():
            return msvcrt.getwch()

        def is_enter(char):
            return char == "\r"

        def is_backspace(char):
            return char == "\b"

    else:
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        def read_char():
            return sys.stdin.read(1)

        def is_enter(char):
            return char in ("\r", "\n")

        def is_backspace(char):
            return char in ("\x7f", "\b")

    if sys.platform != "win32":
        tty.setraw(fd)

    try:
        while True:
            char = read_char()

            if is_enter(char):
                if len(code) == code_length:
                    if secret:
                        print("\r\n", end="", flush=True)
                    else:
                        print(end="\r", flush=True)
                    break

                if sys.platform != "win32":
                    termios.tcsetattr(
                        fd, termios.TCSADRAIN, old_settings
                    )

                print(
                    f"\r\nYour code [{len(code)}] does not match "
                    f"the required code length [{code_length}]!"
                )

                code = ""
                print(prompt, end=" ", flush=True)

                if sys.platform != "win32":
                    tty.setraw(fd)

            elif is_backspace(char):
                if code:
                    code = code[:-1]
                    print("\b \b", end="", flush=True)

            elif char.isdigit() and len(code) < code_length and secret:
                code += char
                print("*", end="", flush=True)

            elif char.isdigit() and len(code) < code_length and not secret:
                code += char
                print(char, end="", flush=True)

    finally:
        if sys.platform != "win32":
            termios.tcsetattr(
                fd, termios.TCSADRAIN, old_settings
            )

    return code

def get_mode(prompt: str, selection: List[str], input_length: int=1) -> str:

    mode = ""
    print(prompt, end=" ", flush=True)

    if sys.platform == "win32":
        import msvcrt

        def read_char():
            return msvcrt.getwch()

        def is_enter(char):
            return char == "\r"

        def is_backspace(char):
            return char == "\b"

    else:
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        def read_char():
            return sys.stdin.read(1)

        def is_enter(char):
            return char in ("\r", "\n")

        def is_backspace(char):
            return char in ("\x7f", "\b")

    if sys.platform != "win32":
        tty.setraw(fd)

    try:
        while True:
            char = read_char()

            if is_enter(char):
                if len(mode) == input_length:
                    print("\r\n", end="", flush=True)
                    break

                if sys.platform != "win32":
                    termios.tcsetattr(
                        fd, termios.TCSADRAIN, old_settings
                    )

                print(
                    f"\r\nYour mode [{len(mode)}] does not match "
                    f"the required mode length [{input_length}]!"
                )

                mode = ""
                print(prompt, end=" ", flush=True)

                if sys.platform != "win32":
                    tty.setraw(fd)

            elif is_backspace(char):
                if mode:
                    mode=mode[:-1]
                    print("\b \b", end="", flush=True)

            elif char in selection and len(mode) < input_length:
                mode+=char
                print(char, end="", flush=True)

    finally:
        if sys.platform != "win32":
            termios.tcsetattr(
                fd, termios.TCSADRAIN, old_settings
            )

    return mode