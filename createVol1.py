import MakePretty


class VolOneCreate(MakePretty):

    def __init__(self, old_version, new_version):
        super(old_version, new_version)
        self.preamble = open("./preambleVolume1.txt", "r")
        self.postamble = open("./postamble.txt", "r")
