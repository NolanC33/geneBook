from src import MakePretty


class VolTwoCreate(MakePretty):

    def __init__(self):
        super().__init__("../mouthOfHorse/v1.txt", "../gen/volume2.tex", "./preambleVolume2.txt", "./postamble.txt")