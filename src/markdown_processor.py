from itertools import filterfalse
from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_blocks(markdown):
    blocks = []
    blocks_cleaned = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        if block == "":
            continue
        if '\n' in block:
            sub_block = list(block.split('\n'))
            for i in range(len(sub_block)):
                sub_block[i] = sub_block[i].strip()
            joined_block = '\n'.join(sub_block)
            block = joined_block
        block = block.strip()
        blocks_cleaned.append(block)
    return blocks_cleaned

def block_to_block_type(block):
    if block.startswith('# ') or block.startswith('## ') or block.startswith('### ') or block.startswith('#### ') or block.startswith('##### ') or block.startswith('###### '):
        return "heading"

    elif block.startswith("```") and block.endswith("```"):
        return "code"

    elif block.startswith('>'):
        pot_quote = list(block.split('\n'))
        for line in pot_quote:
            line = line.strip()
            if line.startswith('>'):
                continue
            else:
                return "paragraph"
        return "quote"

    elif block.startswith("* ") or block.startswith("- "):
        pot_list = list(block.split('\n'))
        for line in pot_list:
            line = line.strip()
            if line.startswith('* ') or line.startswith('- '):
                continue
            else:
                return "paragraph"
        return "unordered_list"

    elif block.startswith('1. '):
        pot_olist = list(block.split('\n'))
        for i, line in enumerate(pot_olist, start=1):
            line = line.strip()
            if line.startswith(f"{i}. "):
                continue
            else:
                return "paragraph"
        return "ordered_list"

    else:
        return "paragraph"


def check_heading(heading):
    x = heading.count('#', 0, 5)
    if x == 1:
        return 'h1'
    elif x == 2:
        return 'h2'
    elif x == 3:
        return 'h3'
    elif x == 4:
        return 'h4'
    elif x == 5:
        return 'h5'
    elif x == 6:
        return 'h6'

def text_to_children(text):
    nested_nodes = []
    sub_nodes = []
    sub_nodes = text.split('\n')
    for sub_node in sub_nodes:
        block_type = block_to_block_type(text)
        if block_type == 'ordered_list' or block_type == 'unordered_list':
            nested_nodes.append(HTMLNode('li', sub_node))
        elif block_type == 'code':
            nested_nodes.append(HTMLNode('code', sub_node.strip('```')))
        elif block_type == 'quote':
            nested_nodes.append(HTMLNode('p', sub_node.strip('> ')))
        elif block_type == 'paragraph':
            nested_nodes.append(HTMLNode('p', sub_node))

    return nested_nodes



def markdown_to_html_node(markdown):
    block_types = []
    blocks = markdown_to_blocks(markdown)
    
    for block in blocks: #Create list of block types
#        print(block)
        block_types.append(block_to_block_type(block))
#    print(blocks)
#    print(block_types)
    nodes = []
    for i, block in enumerate(blocks):
        #HEADING
        if block_types[i] == 'heading':
            heading = check_heading(block)
            stripped_heading = block.strip("#* ")
            nodes.append(HTMLNode(heading, stripped_heading))
#            print(f"nodes = {nodes}")

        #PARAGRAPH
        elif block_types[i] == 'paragraph':
            nodes.append(HTMLNode('p', block))
        
        #CODE
        elif block_types[i] == 'code':
            nodes.append(ParentNode('pre', text_to_children(block)))

        #ORDERED_LIST
        elif block_types[i] == 'ordered_list':
            nodes.append(ParentNode('ol', text_to_children(block)))
#            print(f"node = {sub_nodes}")
#            print(f"sub = {block}")

        #UNORDERED_LIST
        elif block_types[i] == 'unordered_list':
            nodes.append(ParentNode('ul', text_to_children(block)))

        #QUOTE
        elif block_types[i] == 'quote':
            nodes.append(ParentNode('blockquote', text_to_children(block)))

    #WRAP IN DIV
    completed = ParentNode('div', nodes)

    return completed
        
