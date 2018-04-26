
class FalsePositive:

    def __init__(self, word, length):
        self.word = word
        self.length = length

    def is_false_positive(self, line):

        split_version = line.split()

        if len(split_version) == self.length and self.word in line:
            return True

        return False
