from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == "text" and delimiter in node.text:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Invalid Markdown Syntax (No closing delimiter)")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    #Even index, outside the delimiter
                    new_nodes.append(TextNode(part, "text"))
                    #Odd index, inside the delimiter
                else:
                    new_nodes.append(TextNode(part, text_type))
                

        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    extracted = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return extracted





def extract_markdown_links(text):
    extracted = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return extracted

