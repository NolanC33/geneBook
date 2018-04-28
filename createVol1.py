from MakePretty import MakePretty


class VolOneCreate(MakePretty):

    def __init__(self):
        super().__init__("./mouthOfHorse/volume1Prime.txt", "./gen/volume1.tex", "./preambleVolume1.txt", "./postamble.txt")