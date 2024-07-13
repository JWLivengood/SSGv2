import unittest

from htmlnode import HTMLNode

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
