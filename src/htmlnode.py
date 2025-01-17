from enum import Enum

class TagType(Enum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    P = "p"
    DIV = "div"
    SPAN = "span"
    A = "a"
    IMG = "img"
    UL = "ul"
    OL = "ol"
    LI = "li"
    TABLE = "table"
    THEAD = "thead"
    TBODY = "tbody"
    TR = "tr"
    TH = "th"
    TD = "td"
    FORM = "form"
    INPUT = "input"
    BUTTON = "button"
    SELECT = "select"
    OPTION = "option"
    LABEL = "label"
    CANVAS = "canvas"
    SCRIPT = "script"
    STYLE = "style"
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    BLOCKQUOTE = "blockquote"
    HR = "hr"
    BR = "br"
    PRE = "pre"
    

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()]) if self.props else ''

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
        if self.tag is None:
            self.tag = ''
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.children is not None:
            raise ValueError("LeafNode must not have children")
        
    @property
    def children(self):
        return None
        
    @children.setter
    def children(self, value):
        if self.children is not None:
            raise ValueError("LeafNode must not have children")
    
    def to_html(self):
        if self.props and not self.tag:
            return f"<{self.props_to_html()}>{self.value}</{self.tag}>"
        if self.tag and not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        if self.tag and self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"{self.value}"
    
    def is_parent(self):
        return False

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        if not self.tag or not self.children:
            raise ValueError("ParentNode must have a tag and children")

    def is_parent(self):
        return True

    def to_html(self):
        # recurse
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{"".join([child.to_html() for child in self.children])}</{self.tag}>"
        return f"<{self.tag}>{"".join([child.to_html() for child in self.children])}</{self.tag}>"
    

    