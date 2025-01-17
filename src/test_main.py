import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from transformers import text_node_to_html_node




class TestTextToHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node with an  image", TextType.IMAGE, 'https://www.boot.dev')
        htmlnode = text_node_to_html_node(node)
        htmlnode2 = text_node_to_html_node(node2)
        htmlnode3 = text_node_to_html_node(node3)
        self.assertEqual(htmlnode.value, "This is a text node")
        self.assertEqual(htmlnode.tag, 'b')
        self.assertEqual(htmlnode3.props, {'src': 'https://www.boot.dev', 'alt': 'This is a text node with an  image'})
        self.assertEqual(htmlnode3.tag, 'img')



if __name__ == "__main__":
    unittest.main()