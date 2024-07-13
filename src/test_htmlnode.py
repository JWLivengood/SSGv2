import unittest


from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        node1 = HTMLNode("p", "this is an html node", None, {
        "href": "https://www.google.com",
        "target": "_blank",
        })

        pth_t = ' href="https://www.google.com" target="_blank"'
        rpr_t = "HTMLNode(p, this is an html node, children: None, {'href': 'https://www.google.com', 'target': '_blank'}"

        self.assertEqual(node1.props_to_html(), pth_t)
        self.assertEqual(node1.__repr__(), rpr_t)

    def test_values(self):
        node2 = HTMLNode("a", "Wow we are testing", None, {"class": "greeting", "href": "https://boot.dev"})

        self.assertEqual(node2.tag, "a")
        self.assertEqual(node2.value, "Wow we are testing")
        self.assertEqual(node2.children, None)
        self.assertEqual(node2.props, {"class": "greeting", "href": "https://boot.dev"})
        self.assertEqual(node2.props_to_html(), ' class="greeting" href="https://boot.dev"')


class TestLeafNode(unittest.TestCase):
    def test_leafnode(self):
        node = LeafNode("p", "This is a paragraph of text.")
        #print(node.__repr__())
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        #print(f"node2: {node2.__repr__()}")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_valueerror(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_notag(self):
        node = LeafNode(None, "Oops! I forgot a tag!")
        self.assertEqual(node.to_html(), "Oops! I forgot a tag!")


class TestParentNode(unittest.TestCase):
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

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("p", [LeafNode(None, "Normal text"), LeafNode("i", "italic text")]),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
                LeafNode(None, "Normal text"),
            ],
        )
        
        self.assertEqual(node2.to_html(), '<p><b>Bold text</b><p>Normal text<i>italic text</i></p><a href="https://www.google.com">Click me!</a>Normal text</p>')

        node3 = ParentNode("p")
        self.assertRaises(ValueError, node3.to_html)        

        node4 = ParentNode(None, [LeafNode("b", "Bold text")])
        self.assertRaises(ValueError, node4.to_html)
