import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from markdown_processor import markdown_to_blocks, block_to_block_type, markdown_to_html_node

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
        html_test = markdown_to_html_node(block_test)
        expected = ParentNode('div', [HTMLNode('h3', "This is a heading."), 
                    HTMLNode('p', 'This is a paragraph.'), 
                    ParentNode('pre', 
                               [HTMLNode('code', 'This is code.')]),
                    ParentNode('ol', 
                               [HTMLNode('li', '1. this'), 
                                HTMLNode('li', '2. is'), 
                                HTMLNode('li', '3. a'), 
                                HTMLNode('li', '4. list')]
                               ),
                    ParentNode('ul',
                               [HTMLNode('li', '* This'),
                                HTMLNode('li', '* is'),
                                HTMLNode('li', '* unordered'),
                                HTMLNode('li', '- list')]),
                    ParentNode('blockquote', 
                               [HTMLNode('p', 'Now this is a big quote.'),
                                HTMLNode('p', 'And this a lil quote')])
                    ])
        self.assertEqual(expected, html_test) 
