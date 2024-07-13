from textnode import TextNode, text_type_bold
from htmlnode import HTMLNode

def main():
    node = TextNode("This is a text node", text_type_bold, "https://www.google.com")
    print(node)

    node2 = HTMLNode("this is an html node", "p", None, {
    "href": "https://www.google.com", 
    "target": "_blank",
})

    print(node2)

    node2.props_to_html()
main()
