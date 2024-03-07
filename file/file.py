import io
from dataclasses import dataclass
import os


@dataclass
class File:
    filename: str
    writeable: bool = False
    binary: bool = False
    file_object: io.IOBase = None

    def open(self):
        if self.writeable:
            mode = "w"
        else:
            mode = "r"
        if self.binary:
            mode += "b"

        self.file_object = open(self.filename, mode)

    def write(self, text: str):
        if not self.writeable:
            raise NotImplementedError("cannot write to readable object")
        self.file_object.write(text)

    def writeln(self, text: str):
        if not self.writeable:
            raise NotImplementedError("cannot write to readable object")
        self.file_object.write(text + "\n")

    def __enter__(self):
        # self.__init__(filename, writeable, binary)
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_object.close()
        return
