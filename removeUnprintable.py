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
        cleaned = ''.join(filter(lambda x: x in self.printable, line))

        if MakePretty.check_if_removable(cleaned):
            return ''

        return MakePretty.escape_bad_chars(cleaned)

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

        if len(split_version) == 3 and "CRANE GENEALOGY." in line:
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
