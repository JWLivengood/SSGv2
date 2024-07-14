import unittest

from textnode import TextNode, text_node_to_html_node, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
from htmlnode import HTMLNode, LeafNode, ParentNode

from splitnodes import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

        node3 = TextNode("This too is a text node", "text")
        node4 = TextNode("And so too is this", "text")
        self.assertNotEqual(node3, node4)

        node5 = TextNode("Now we are testing links", "text", "https://www.google.com")
        node6 = TextNode("Now we are testing links", "text", "https://www.google.com")
        self.assertEqual(node5, node6)

        node7 = TextNode("Let's test different text types", "bold", None)
        node8 = TextNode("Let's test different text types", "italic", None)
        self.assertNotEqual(node7, node8)

    def test_textnode_to_htmlnode(self):
        i_node = TextNode("Testing", "text")
        node1 = text_node_to_html_node(i_node)
        node2 = LeafNode(None, "Testing", None)
        #print(html_node)
        self.assertEqual(node1.tag, node2.tag)
        self.assertEqual(node1.value, node2.value)
        self.assertEqual(node1.children, node2.children)
        self.assertEqual(node1.props, node2.props)


        i_node3 = TextNode("This node is testing bold text", "bold")
        node3 = text_node_to_html_node(i_node3)
        node4 = LeafNode("b", "This node is testing bold text")
        
        self.assertEqual(node3.tag, node4.tag)
        self.assertEqual(node3.value, node4.value)
        self.assertEqual(node3.children, node4.children)
        self.assertEqual(node3.props, node4.props)


        i_node5 = TextNode("This node is testing italic text", "italic")
        node5 = text_node_to_html_node(i_node5)
        node6 = LeafNode("i", "This node is testing italic text")
        
        self.assertEqual(node5.tag, node6.tag)
        self.assertEqual(node5.value, node6.value)
        self.assertEqual(node5.children, node6.children)
        self.assertEqual(node5.props, node6.props)


        i_node7 = TextNode("Testing Code Text", "code")
        node7 = text_node_to_html_node(i_node7)
        node8 = LeafNode("code", "Testing Code Text")

        self.assertEqual(node7.tag, node8.tag)
        self.assertEqual(node7.value, node8.value)
        self.assertEqual(node7.children, node8.children)
        self.assertEqual(node7.props, node8.props)


        i_node9 = TextNode("Testing Link Text", "link", "https://www.google.com")
        node9 = text_node_to_html_node(i_node9)
        node10 = LeafNode("a", "Testing Link Text", {"href": "https://www.google.com"})

        self.assertEqual(node9.tag, node10.tag)
        self.assertEqual(node9.value, node10.value)
        self.assertEqual(node9.children, node10.children)
        self.assertEqual(node9.props, node10.props)


        i_node11 = TextNode("Testing Image Text", "image", "https://picsum.photos/200/300")
        node11 = text_node_to_html_node(i_node11)
        node12 = LeafNode("img", "", {"src": "https://picsum.photos/200/300", "alt": "Testing Image Text"})

        self.assertEqual(node11.tag, node12.tag)
        self.assertEqual(node11.value, node12.value)
        self.assertEqual(node11.children, node12.children)
        self.assertEqual(node11.props, node12.props)

        node13 = TextNode("Testing failed text", "dummy")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node13)
        self.assertEqual(str(context.exception), "TextNode's text type not recognized")

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", text_type_text),
                    TextNode("code block", text_type_code),
                    TextNode(" word", text_type_text),
                ],
                new_nodes,
            )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another** as well.", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
                [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
                TextNode(" as well.", text_type_text)
                ],
                new_nodes,
            )


    def test_bold_and_italic(self):
        node = TextNode("This time we have **bold** and *italic* text.", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertEqual(
                [
                TextNode("This time we have ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" text.", text_type_text)
                ],
                new_nodes,
            )








if __name__ == "__main__":
    unittest.main()
