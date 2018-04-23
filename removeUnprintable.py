import string
import os


class MakePretty:
    oldVersion = open("./v1.txt", 'r')
    newVersion = open("./v2.txt", 'w+', encoding='utf-8')
    printable = set(string.printable)

    def __init__(self):
        self.printable.add("£")

    def peek_old_line(self):
        pos = self.oldVersion.tell()
        line = self.oldVersion.readline()
        self.oldVersion.seek(pos)
        return line

    def clean_line(self, line):
        return ''.join(filter(lambda x: x in self.printable, line))

    def convert(self):
        this_line = self.oldVersion.readline().strip()

        while this_line:
            fixed_line = self.clean_line(this_line)
            next_line = self.peek_old_line().strip()

            while next_line:
                fixed_line += self.clean_line(' ' + next_line)
                self.oldVersion.readline()
                next_line = self.peek_old_line().strip()

            self.newVersion.write(fixed_line)
            this_line = self.oldVersion.readline()

        self.oldVersion.close()
        self.newVersion.close()


mp = MakePretty()

mp.convert()
