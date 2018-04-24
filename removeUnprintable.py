import string


class MakePretty:
    oldVersion = open("./v1.txt", 'r')
    newVersion = open("./v2.tex", 'w+', encoding='utf-8')
    printable = set(string.printable)

    def __init__(self):
        self.printable.add("£")

    def peek_old_line(self):
        pos = self.oldVersion.tell()
        line = self.oldVersion.readline()
        self.oldVersion.seek(pos)
        return line

    def clean_and_parse_line(self, line):

        if not line.strip():
            return line

        cleaned = ''.join(filter(lambda x: x in self.printable, line))

        if MakePretty.check_if_removable(cleaned):
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

        things_to_escape = ["\\", "&", "%", "$", "#", "_", "^"]

        for rep in things_to_escape:
            new_line = new_line.replace(rep, "\\" + rep)

        return new_line

    @staticmethod
    def check_if_removable(line):
        split_version = line.strip().split(" ")

        if len(split_version) == 3 and "GENEALOGY." in line:
            return True

        if len(split_version) == 2 and "ADDENDA." in line:
            return True

        return False

    def generate(self):
        self.oldVersion = open("./v1.txt", 'r')
        self.newVersion = open("./v2.tex", 'w+', encoding='utf-8')

        preamble = open("./preamble.txt", "r")
        postamble = open("./postamble.txt", "r")

        self.newVersion.write(preamble.read())

        self.convert()

        self.newVersion.write(postamble.read())

        self.oldVersion.close()
        self.newVersion.close()

        preamble.close()
        postamble.close()

    def convert(self):

        this_line = self.oldVersion.readline()

        while this_line:
            fixed_line = self.clean_and_parse_line(this_line)
            if fixed_line:
                self.newVersion.write(fixed_line)
            this_line = self.oldVersion.readline()



MakePretty().generate()
