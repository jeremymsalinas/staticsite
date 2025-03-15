import os, shutil, sys
from textnode import TextNode, TextType, Delimiters
from transformers import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def copy_contents(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    

    NewNode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(repr(NewNode))
    copy_contents('static', 'public')
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)



if __name__ == '__main__':
    main()