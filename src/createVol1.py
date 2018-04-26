from gen import MakePretty


class VolOneCreate(MakePretty):

    def __init__(self, old_version, new_version):
        super("../mouthOfHorse/volume1.txt", "../gen/volume1.tex")
        self.preamble = open("./preambleVolume1.txt", "r")
        self.postamble = open("./postamble.txt", "r")
