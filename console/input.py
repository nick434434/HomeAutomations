import os
from dataclasses import dataclass
import sys
import select


@dataclass
class NonBlockingConsole:

    def __enter__(self):
        if self.is_linux:
            import termios
            import tty
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        if self.is_linux:
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    @property
    def is_windows(self):
        return os.name == "nt"

    @property
    def is_linux(self):
        return os.name == "posix"

    def get_data(self):
        if self.is_linux:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return sys.stdin.read(1)
        if self.is_windows:
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getch().decode()
        return None

    def get_enter(self):
        char = self.get_data()
        return char == '\r' or char == '\n'

    def get_q(self):
        return self.get_data() == 'q'
