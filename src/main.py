from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
from htmlnode import HTMLNode
from splitnodes import split_nodes_delimiter, extract_markdown_images
from setstatic import source_to_public, generate_pages_recursive


def main():

    source_to_public('/Users/jlivengood/workspace/github.com/JWLivengood/SSGv2/static', '/Users/jlivengood/workspace/github.com/JWLivengood/SSGv2/public/')

    generate_pages_recursive('/Users/jlivengood/workspace/github.com/jwlivengood/ssgv2/content/', '/Users/jlivengood/workspace/github.com/jwlivengood/ssgv2/template.html', '/Users/jlivengood/workspace/github.com/JWLivengood/SSGv2/public/')

main()


