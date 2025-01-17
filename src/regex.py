import re


class RegexIn(str):

    def __eq__(self, pattern):
        return re.match(pattern, self)