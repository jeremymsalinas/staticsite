from transformers import *
import unittest



class TestTransformers(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        nodes = [
            TextNode("This is plain text", TextType.TEXT),
            TextNode("This is *italic* text", TextType.TEXT),
            ]
        result2 = [
            TextNode("This is plain text", TextType.TEXT),
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        new_nodes2 = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, result)
        self.assertEqual(new_nodes2, result2)

    def test_text_node_to_html_node(self):
        node = TextNode('I like Tolkien', TextType.BOLD, None)
        result = LeafNode('b','I like Tolkien')
        self.assertEqual(repr(text_node_to_html_node(node)), repr(result))


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), result)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), result)

    def test_split_nodes_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode(
            "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            ]
        self.assertEqual(split_nodes_link([TextNode(text, TextType.TEXT)]), result)

    def test_split_nodes_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ", TextType.TEXT),
        TextNode(
            "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            ]
        self.assertEqual(split_nodes_image([TextNode(text, TextType.TEXT)]), result)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), result)
    
    def test_markdown_to_blocks(self):
        text = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        self.assertEqual(markdown_to_blocks(text),result)
    
    def test_block_to_block_type(self):
        blocks = [
            "# This is a heading",
            "### This is a heading",
            "#### This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            "1. This is the first list item in an ordered list block\n2. This is a list item\n3. This is another list item",
            "```this is a code block```",
            ">This is a quote block\n>This is another line\n>and another line",
            "**Bold** text\n*Italic* text in a paragraph",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        self.assertEqual(block_to_block_type(blocks[0]), 'h1')
        self.assertEqual(block_to_block_type(blocks[1]), 'h3')
        self.assertEqual(block_to_block_type(blocks[2]), 'h4')
        self.assertEqual(block_to_block_type(blocks[3]), 'p')
        self.assertEqual(block_to_block_type(blocks[4]), 'ul')
        self.assertEqual(block_to_block_type(blocks[5]), 'ol')
        self.assertEqual(block_to_block_type(blocks[6]), 'code')
        self.assertEqual(block_to_block_type(blocks[7]), 'blockquote')
        self.assertEqual(block_to_block_type(blocks[8]), 'p')
        self.assertEqual(block_to_block_type(blocks[9]), 'ul')


    def test_block_to_html_node(self):
        blocks = [
            "# This is a heading",
            "### This is a heading",
            "#### This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            "1. This is the first list item in an ordered list block\n2. This is a list item\n3. This is another list item",
            "```this is a code block```",
            ">This is a quote block\n>This is another line\n>and another line",
            "**Bold** text\n*Italic* text in a paragraph",
            ]
        self.assertEqual(repr(block_to_html_node('h1', blocks[0])), repr(LeafNode('h1', 'This is a heading')))
        self.assertEqual(repr(block_to_html_node('h3', blocks[1])), repr(LeafNode('h3', 'This is a heading')))
        self.assertEqual(repr(block_to_html_node('h4', blocks[2])), repr(LeafNode('h4', 'This is a heading')))
        self.assertEqual(repr(block_to_html_node('p', blocks[3])), repr(LeafNode('p', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.')))
        self.assertEqual(repr(block_to_html_node('ul', blocks[4])), repr(LeafNode('ul', 'This is the first list item in a list block\nThis is a list item\nThis is another list item')))
        self.assertEqual(repr(block_to_html_node('ol', blocks[5])), repr(LeafNode('ol', 'This is the first list item in an ordered list block\nThis is a list item\nThis is another list item')))
        self.assertEqual(repr(block_to_html_node('code', blocks[6])), repr(LeafNode('code', 'this is a code block')))
        self.assertEqual(repr(block_to_html_node('blockquote', blocks[7])), repr(LeafNode('blockquote', 'This is a quote block\nThis is another line\nand another line')))
        self.assertEqual(repr(block_to_html_node('p', blocks[8])), repr(LeafNode('p', '**Bold** text\n*Italic* text in a paragraph')))
        
        with self.assertRaises(ValueError):
            block_to_html_node('x','<x>This is an invalid block')

    def test_markdown_to_html_node(self):
        text = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        self.assertEqual(repr(markdown_to_html_node(text)),repr(ParentNode('div',children=[
            LeafNode('h1','This is a heading'),
            LeafNode('p','This is a paragraph of text. It has some **bold** and *italic* words inside of it.'),
            LeafNode('ul','This is the first list item in a list block\nThis is a list item\nThis is another list item')])))
