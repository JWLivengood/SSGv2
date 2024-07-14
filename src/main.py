from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
from htmlnode import HTMLNode
from splitnodes import split_nodes_delimiter, extract_markdown_images


def main():

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    print(extract_markdown_images(text))


main()


