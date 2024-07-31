from itertools import filterfalse
from textnode import TextNode, text_node_to_html_node, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitnodes import text_to_textnodes

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


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
#    print(f"blocks = {blocks}")
    for block in blocks:
        if block[0:5].count("#") != 1:
            continue
        else:
            title = block[1:]
    return title

def markdown_to_html(markdown):
    return markdown_to_text_nodes(markdown).to_html()

def markdown_to_text_nodes(markdown):
    blocks = markdown_to_blocks(markdown)
#    print(f"blocks = {blocks}")
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
#        print(f"html_node = {html_node}")
        if html_node:
            children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == 'paragraph':
        return paragraph_to_html_node(block)
    if block_type == 'heading':
        return heading_to_html_node(block)
    if block_type == 'code':
        return code_to_html_node(block)
    if block_type == 'ordered_list':
        return olist_to_html_node(block)
    if block_type == 'unordered_list':
        return ulist_to_html_node(block)
    if block_type == 'quote':
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
#    print(f"Original Block: {block}")
    lines = block.split('\n')
    children = []

    for line in lines:
        children.extend(text_to_children(line))
        children.append(LeafNode('br', ""))

    if children and isinstance(children[-1], LeafNode) and children[-1].tag == 'br':
        children.pop()

    if not children:
        return LeafNode('p', block)
    return ParentNode('p', children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    if level +1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[3:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

