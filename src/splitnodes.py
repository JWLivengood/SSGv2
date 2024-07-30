from textnode import TextNode, text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
#    print(f"old_nodes = {old_nodes}")
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError(f"Expected TextNode, but got {type(node)} with value {node}")
#        print(f"node = {node}")
        if node.text_type == "text" and delimiter in node.text:
            parts = node.text.split(delimiter)
#            print(f"Split result at '{delimiter}': {parts}")
            if len(parts) % 2 == 0:
                raise Exception(f"Invalid Markdown Syntax (No closing delimiter for {delimiter})")
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


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == "image":
            new_nodes.append(node)
            continue

        extracted = extract_markdown_links(node.text)
        if extracted == []:
            new_nodes.append(TextNode(node.text, node.text_type))
#            return new_nodes
        else:
            remaining_text = node.text
            for i, link in enumerate(extracted):
                parts = remaining_text.split(f"[{extracted[i][0]}]({extracted[i][1]})", 1)

#                print(f"\n{i}, parts = {parts}")
#                print(f"{i}, remaining text = {remaining_text}")
#                print(f"extracted = {extracted}")

                if parts[0] == "":
                    new_nodes.append(TextNode(extracted[i][0], "link", extracted[i][1]))
                else:
                    new_nodes.append(TextNode(parts[0], "text"))
                    new_nodes.append(TextNode(extracted[i][0], "link", extracted[i][1]))

#                print(f"current_node = {new_nodes}")
                if i == (len(extracted) - 1) and parts[1] != "":
                    new_nodes.append(TextNode(parts[1], "text"))
                else:
                    remaining_text = parts[1]
#    print(f"new_nodes = {new_nodes}")
    return new_nodes



def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == "link":
            new_nodes.append(node)
            continue

        extracted = extract_markdown_images(node.text)
        if extracted == []:
            new_nodes.append(TextNode(node.text, node.text_type))
#            return new_nodes
        else:
            remaining_text = node.text
            for i, (alt_text, url) in enumerate(extracted):
                parts = remaining_text.split(f"![{extracted[i][0]}]({extracted[i][1]})", 1)

#                print(f"\n{i}, parts = {parts}")
#                print(f"{i}, remaining text = {remaining_text}")
#                print(f"extracted = {extracted}")

                if parts[0] == "":
                    new_nodes.append(TextNode(extracted[i][0], "image", extracted[i][1]))
#                    print(f"Creating image node with: ({extracted[i][0]}, 'image', {extracted[i][1]})")
                else:
                    new_nodes.append(TextNode(parts[0], "text"))
                    new_nodes.append(TextNode(extracted[i][0], "image", extracted[i][1]))
#                    print(f"Creating image node with: ({extracted[i][0]}, 'image', {extracted[i][1]})")

#                print(f"current_node = {new_nodes}")
                if i == (len(extracted) - 1) and parts[1] != "":
                    new_nodes.append(TextNode(parts[1], "text"))
                else:
                    remaining_text = parts[1]
#    print(f"new_nodes = {new_nodes}")
    return new_nodes

def text_to_textnodes(text):
    if isinstance(text, str):
        new_nodes = [TextNode(text, "text")]
    else:
        new_nodes = text
#    print(f"Initial TextNode: {new_nodes}") #Debug

    new_nodes1 = split_nodes_delimiter(new_nodes, "**", text_type_bold)
#    print(f"After splitting **: {new_nodes1}")

    new_nodes2 = split_nodes_delimiter(new_nodes1, "*", text_type_italic)
#    print(f"After splitting *: {new_nodes2}")

    new_nodes3 = split_nodes_delimiter(new_nodes2, "'", text_type_code)
#    print(f"After splitting ': {new_nodes3}")

    new_nodes4 = split_nodes_image(new_nodes3)
#    print(f"After splitting image: {new_nodes4}")

    new_nodes5 = split_nodes_link(new_nodes4)
#    print(f"After splitting link: {new_nodes5}")
#    print(f"1: {new_nodes1}")
#    print(f"2: {new_nodes2}")
#    print(f"3: {new_nodes3}")
#    print(f"4: {new_nodes4}")
#    print(f"5: {new_nodes5}")
    return new_nodes5
