import re


class BlockPatterns:
    HEADER = re.compile(r'^(#){1,6}\s')