import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node3 = HTMLNode()
        node2 = HTMLNode("p","This is a test paragraph",[node3])
        node = HTMLNode("h1","This is a test header", [node2,node3], {"href": "https://www.google.com","target": "_blank"})
        leafnode = LeafNode(node.tag, node.value, node.props)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "This is a test header")
        self.assertEqual(node.children, [node2, node3])
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')
        self.assertIsNone(node2.props)
        self.assertIsNone(node3.tag)
        self.assertIsNone(node3.value)
        self.assertIsNone(node3.children)
        
    
    def test_leafnode(self):
        node3 = HTMLNode()
        node2 = HTMLNode("p","This is a test paragraph",[node3])
        node = HTMLNode("h1","This is a test header", [node2,node3], {"href": "https://www.google.com","target": "_blank"})
        leafnode = LeafNode(node.tag, node.value, node.props)
        leafnode2 = LeafNode("p", "This is a paragraph of text.")
        leafnode3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertIsNone(leafnode.children)
        self.assertEqual(leafnode.to_html(),'<h1 href="https://www.google.com" target="_blank">This is a test header</h1>')
        self.assertEqual(leafnode2.to_html(),'<p>This is a paragraph of text.</p>')
        self.assertEqual(leafnode3.to_html(),'<a href="https://www.google.com">Click me!</a>')
        leafnode.children = [1,2,3]
        self.assertEqual(leafnode.children, None)
    
    def test_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node2 = ParentNode(
            'div',
            [
                node,
                ParentNode(
                    'div',
                    [
                        LeafNode("title", "This is a title"),
                        LeafNode("h1", "This is a header"),
                        LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
                        LeafNode("p", "This is a paragraph of text.")
                    ]
                ),
                LeafNode("p", "This is a another paragraph of text.")
            ]
        )
        self.assertEqual(node.to_html(),'<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
        self.assertEqual(node2.to_html(),'<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><div><title>This is a title</title><h1>This is a header</h1><a href="https://www.google.com">Click me!</a><p>This is a paragraph of text.</p></div><p>This is a another paragraph of text.</p></div>')

if __name__ == "__main__":
    unittest.main()