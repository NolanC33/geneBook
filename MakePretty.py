import string
import fp


class MakePretty:
    printable = set(string.printable)

    def __init__(self, old_version_path, new_version_path, preamble_path, postamble_path):
        self.printable.add("£")
        self.oldVersion = open(old_version_path, 'r')
        self.newVersion = open(new_version_path, 'w+', encoding='utf8')
        self.false_pos_checkers = []
        self.create_false_positive_checkers()
        self.preamble = open(preamble_path, 'r')
        self.postamble = open(postamble_path, 'r')

    def create_false_positive_checkers(self):

        words = ["GENEALOGY.", "GENERATION.", "ADDENDA.", "ELLERY", "II.", "I."]
        lengths = [3, 3, 2, 3, 2, 2]

        for i in range(len(words)):
            self.false_pos_checkers.append(fp.FalsePositive(words[i], lengths[i]))

    def peek_old_line(self):
        pos = self.oldVersion.tell()
        line = self.oldVersion.readline()
        self.oldVersion.seek(pos)
        return line

    def clean_and_parse_line(self, line):

        if not line.strip():
            return line

        cleaned = ''.join(filter(lambda x: x in self.printable, line))

        if self.check_if_removable(cleaned):
            return ''

        escaped = MakePretty.escape_bad_chars(cleaned)

        if MakePretty.assess_if_heading(line):

            if MakePretty.assess_if_section(line):
                return MakePretty.make_section(escaped)

            return MakePretty.make_chapter(escaped)

        return escaped

    @staticmethod
    def has_numbers(line):
        return any(char.isdigit() for char in line)

    @staticmethod
    def make_chapter(line):

        if "GENERATION" not in line:
            return "\chapter{" + line.strip() + "}"

        return line

    @staticmethod
    def assess_if_heading(line):

        if not line.strip():
            return False

        if " " not in line:
            return False

        if len(line.split()) == 1:
            return False

        if MakePretty.has_numbers(line):
            return False

        if line.count(".") > 1:
            return False

        if not line.isupper():
            return False

        if "GENEALOGY" in line:
            return False

        return True

    @staticmethod
    def assess_if_section(line):
        return "GENERATION" in line

    @staticmethod
    def make_section(line):

        split_line = line.split()

        return "\\section{" + split_line[0] + " " + split_line[1] + "}"

    @staticmethod
    def escape_bad_chars(line):

        new_line = line

        new_line = new_line.replace("^", "\'")
        new_line = new_line.replace("''", "\"")

        things_to_escape = ["\\", "&", "%", "$", "#", "_", "}", "{"]

        for rep in things_to_escape:
            new_line = new_line.replace(rep, "\\" + rep)

        return new_line

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def check_if_removable(self, line):

        split_line = line.split()
        firstWord = split_line[0]
        lastWord = split_line[len(split_line) - 1]

        if MakePretty.is_number(firstWord) or MakePretty.is_number(lastWord):
            return True

        for checker in self.false_pos_checkers:
            if checker.is_false_positive(line):
                return True

        return False

    def generate(self):

        self.newVersion.write(self.preamble.read())

        self.convert()

        self.newVersion.write(self.postamble.read())

        self.oldVersion.close()
        self.newVersion.close()

        self.preamble.close()
        self.postamble.close()

    def convert(self):

        this_line = self.oldVersion.readline()

        while this_line:
            fixed_line = self.clean_and_parse_line(this_line)
            if fixed_line:
                self.newVersion.write(fixed_line)
            this_line = self.oldVersion.readline()
