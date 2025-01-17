from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "normal"

class Delimiters(Enum):
    BOLD = "**"
    ITALIC = "*"
    CODE = "`"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.url = url
        self.text_type = text_type


    def __eq__(self, other):
        return self.__dict__ == other.__dict__  if type(self) == type(other) else False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"