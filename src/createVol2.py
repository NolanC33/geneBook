from gen import MakePretty


class VolTwoCreate(MakePretty):

    def __init__(self):
        super("../mouthOfHorse/v1.txt", "../gen/volume2.tex")
        self.preamble = open("./preambleVolume2.txt", "r")
        self.postamble = open("./postamble.txt", "r")
