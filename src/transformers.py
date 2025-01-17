from textnode import TextNode, TextType, Delimiters
from htmlnode import HTMLNode, LeafNode, ParentNode, TagType
from markdown import BlockPatterns
from regex import RegexIn
import re, os


def text_node_to_html_node(text_node):
    tags = {
        TextType.NORMAL.value: '', 
        TextType.BOLD.value: TagType.BOLD.value,
        TextType.ITALIC.value: TagType.ITALIC.value, 
        TextType.CODE.value: TagType.CODE.value, 
        TextType.LINK.value: TagType.A.value, 
        TextType.IMAGE.value: TagType.IMG.value
        }
    if text_node.text_type.value in tags.keys():
        if text_node.text_type == TextType.IMAGE:
            return LeafNode(tags[text_node.text_type.value],'',{"src": text_node.url, "alt": text_node.text})
        if text_node.text_type == TextType.LINK:
            return LeafNode(tags[text_node.text_type.value],text_node.text,{"href": text_node.url})
        return LeafNode(tags[text_node.text_type.value], text_node.text)
    return LeafNode(None, text_node.text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for x in old_nodes:
        new_text = x.text.split(delimiter)
        if len(new_text) > 1:
            new_nodes.extend(
                [TextNode(new_text[y],TextType.TEXT,x.url) if y % 2 == 0
                else TextNode(new_text[y],text_type,x.url) 
                for y,z in enumerate(new_text)])
        else:
            new_nodes.append(x)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"\((.*?)\)", text)
    alt_texts = re.findall(r"!\[(.*?)\]", text)
    return list(zip(alt_texts, images))

def extract_markdown_links(text):
    texts = re.findall(r"(?<!!)\[(.*?)\]", text)
    links = re.findall(r"\((.*?)\)", text)
    return list(zip(texts, links))

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    # This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
    delimiters = {'**': TextType.BOLD, '*': TextType.ITALIC, '`': TextType.CODE}
    new_nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, text_type in delimiters.items():
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type)
    new_nodes = split_nodes_link(split_nodes_image(new_nodes))
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = []
    cur_group = ''
    for i,line in enumerate(markdown.splitlines()):
        if line:
            if not cur_group:
                cur_group += line.strip()
            else:
                cur_group += '\n'
                cur_group += line.strip()
            if i == len(markdown.splitlines())-1:
                blocks.append(cur_group)
        else:
            blocks.append(cur_group)
            cur_group = ''

    return blocks

def block_to_block_type(block):
    match RegexIn(block):
        case r'^(#){1,6}\s':
            return f'h{len(block.split()[0])}'
        case r'^[*-]\s':
            if all(p.strip().startswith(('*', '-')) for p in block.split('\n')):
                return 'ul'
        case r'^\d+\.\s':
            ordered_list = block.split('\n')
            if list(range(1,len(ordered_list)+1)) == list(map(int, [num[0] for num in ordered_list])):
                return 'ol'
        case r'^>':
            if all(p.startswith('>') for p in block.split('\n')):
                return 'blockquote'
        case r'^```.*(?:\n^\t.*)*':
            return 'pre'
        case _:
            return 'p'

def block_to_html_node(block_type,block):
    sub = lambda x,y,z: f'<{z}>'.join(list(map(lambda x: f'{x.strip()}</{z}>' if x else '', re.split(x,y))))
    get_text_nodes = lambda x: text_to_textnodes(x)
    get_html_nodes = lambda x: list(map(text_node_to_html_node, get_text_nodes(x)))
    map_html = lambda x: "".join(list(map(lambda x: x.to_html(), x))).strip()
    
    match block_type:
        case 'ul':
            items = [line.strip()[2:] for line in block.split('\n')]
            list_content = '\n'.join([f'<li>{map_html(get_html_nodes(item))}</li>' for item in items])
            return LeafNode(block_type, list_content)
        case 'ol':
            new_block = sub(r'\d+\.\s',block,'li')
            return LeafNode(block_type,map_html(get_html_nodes(new_block)))
        case 'p':
            new_block = map_html(get_html_nodes(block))
            return LeafNode(block_type, new_block)
        case 'pre':
            new_block = '\n'.join(re.split(r'```',block))
            return LeafNode(block_type,map_html(get_html_nodes(new_block)))
        case 'blockquote':
            new_block = re.sub(r'>','',block)
            return LeafNode(block_type,map_html(get_html_nodes(new_block)))
        case _:
            new_block = ' '.join(block.split()[1:])
            return LeafNode(TagType(block_type).value,map_html(get_html_nodes(new_block)))

    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return ParentNode('div',children=[block_to_html_node(block_to_block_type(block),block) for block in blocks])

def extract_title(markdown):
    text = re.match(r'#\s(.*)\n',markdown)
    if not text:
        raise ValueError("Invalid markdown, no title found")
    return text.group(1)



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}")
    
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    with open(from_path, 'r') as from_file:
        content = from_file.read()

    title = extract_title(content)
    html_node = markdown_to_html_node(content)
    children = html_node.children

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html_node.to_html())

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))


    with open(dest_path, 'w') as dest_file:
        dest_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir):
    print(f"Generating pages from {dir_path_content} to {dest_dir}")

    with open(template_path, 'r') as template_file:
        template = template_file.read()

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    contents = os.listdir(dir_path_content)
    for filename in contents:
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir, filename.replace('.md', '.html'))
        if os.path.isfile(from_path):
            if filename.endswith('.md'):
                generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)