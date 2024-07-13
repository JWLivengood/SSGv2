import unittest

from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image

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


        
if __name__ == "__main__":
    unittest.main()
