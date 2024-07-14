from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
from htmlnode import HTMLNode
from splitnodes import split_nodes_delimiter



def main():
    

    node = TextNode("This is text with a `code block` word", text_type_text)
    #    node2 = TextNode("This is just text", text_type_text)
    #nodes = [node, node2]
    split_nodes_delimiter([node], "`", text_type_code)


main()


