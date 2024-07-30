import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from markdown_processor import markdown_to_blocks, block_to_block_type, markdown_to_text_nodes, markdown_to_html
from textnode import text_node_to_html_node

class TestMarkdownProcessor(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = (
                    '''
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
                    ''')
        expected_blocks = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ]

        result = markdown_to_blocks(markdown)
        self.assertListEqual(expected_blocks, result)

    def test_block_to_block_type(self):
        block1 = '''# This is a heading.'''
        result1 = block_to_block_type(block1)
        self.assertEqual(result1, "heading")

        block2 = '''####### This is a paragraph'''
        result2 = block_to_block_type(block2)
        self.assertEqual(result2, "paragraph")

        block3 = '''```This is code```'''
        result3 = block_to_block_type(block3)
        self.assertEqual(result3, "code")

        block4 = '''>This is a quote.
>Still Quote.
>We are quoting.
>Much Quote.'''
        result4 = block_to_block_type(block4)
        self.assertEqual(result4, "quote")
        
        block5 = '''1. Welcome
2. To
3. The
4. Jungle'''
        result5 = block_to_block_type(block5)
        self.assertEqual(result5, "ordered_list")

        block6 = '''* This time
* There is no
- order'''
        result6 = block_to_block_type(block6)
        self.assertEqual(result6, "unordered_list")

        block7 = '''>Fake quote
>this gon be fake
this is fake'''
        result7 = block_to_block_type(block7)
        self.assertEqual(result7, "paragraph")


    def test_markdown_to_html_node(self):
        expected = []
        block_test = '''### This is a heading.

                            This is a paragraph.

        ```This is code.```

        1. this
        2. is
        3. a
        4. list

        * This
        * is
        * unordered
        - list

        > Now this is a big quote.
        > And this a lil quote'''
        result = markdown_to_html(block_test)
        
        expected = '<div><h3>This is a heading.</h3><p>This is a paragraph.</p><pre><code>This is code.</code></pre><ol><li>this</li><li>is</li><li>a</li><li>list</li></ol><ul><li>This</li><li>is</li><li>unordered</li><li>list</li></ul><blockquote>Now this is a big quote. And this a lil quote</blockquote></div>'
        self.assertEqual(expected, result)
