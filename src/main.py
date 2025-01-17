import os, shutil
from textnode import TextNode, TextType, Delimiters
from transformers import *


def copy_contents(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)





def main():
    NewNode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(repr(NewNode))
    copy_contents('static', 'public')
    generate_pages_recursive('content/', 'template.html', 'public/')



if __name__ == '__main__':
    main()