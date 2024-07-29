class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        html_string = ""
        for (key, value) in self.props.items():
            html_string += f' {key}="{value}"'
        return html_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props}"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
                self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        self.children = []

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, children: {self.children}, {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == [] or self.children == None:
            raise ValueError("ParentNode must have children")

        child_strings = ""
        for child in self.children:
            child_strings += child.to_html()

        return f'<{self.tag}>{child_strings}</{self.tag}>'

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, children: {self.children}, {self.props}"
