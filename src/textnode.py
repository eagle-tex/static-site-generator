from typing import List
from leafnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        if self.url is None:
            return f"TextNode({self.text}, {self.text_type})"
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self):
        if self.text_type == "text":
            return LeafNode(None, self.text)
        elif self.text_type == "bold":
            return LeafNode("b", self.text)
        elif self.text_type == "italic":
            return LeafNode("i", self.text)
        elif self.text_type == "code":
            return LeafNode("code", self.text)
        elif self.text_type == "link":
            return LeafNode("a", self.text, props={"href": self.url})
        elif self.text_type == "image":
            return LeafNode("img", "", props={"src": self.url, "alt": self.text})
        raise Exception(f"<{(self.text_type).upper()}> is an invalid TextNode type")


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: str
) -> List[TextNode]:
    """
    Split nodes into TextNodes based on the provided delimiter

    Parameters
    ----------
    old_nodes : list of TextNodes of type "text"
        list of nodes to split
    delimiter : str
        the delimiter by which to split
    text_type : str
        the text_type of the resulting TextNode enclosed inside the two <delimiter>s

    Returns
    -------
    TextNode[]
        A list of TextNodes
    """

    if not isinstance(old_nodes, list):
        raise Exception("The first argument of split_nodes_delimiter must be a list")

    def parse_nodes(old_nodes):
        new_nodes = []
        for node in old_nodes:
            if isinstance(node, TextNode) and node.text_type == "text":
                parts = node.text.split(delimiter)

                # If a delimiter is missing, raise a ValueError
                if len(parts) % 2 == 0:
                    raise ValueError(
                        f"Unmatched delimiter '{delimiter}' found in text: {node.text}"
                    )

                # Go through parts and create appropriate TextNodes
                for i, part in enumerate(parts):
                    if i % 2 == 0:  # Even indexes: normal text
                        new_nodes.append(TextNode(part, "text"))
                    else:  # Odd indexes: delimited text
                        new_nodes.append(TextNode(part, text_type))

            else:
                # Directly add non-text or non-splittable nodes
                new_nodes.append(node)

        return new_nodes

    # def text_to_textnode(input_text: str):
    #     output = ""
    #     if not isinstance(input_text, str):
    #         raise ValueError("The input of 'text_to_text_node' must be a string")
    #
    #     if input_text.startswith("**") and input_text.endswith("**"):
    #         output = TextNode(input_text, "bold")
    #     elif input_text.startswith("*") and input_text.endswith("*"):
    #         output = TextNode(input_text, "italic")
    #     elif input_text.startswith("`") and input_text.endswith("`"):
    #         output = TextNode(input_text, "code")
    #     else:
    #         output = TextNode(input_text, "text")
    #
    #     return output

    return parse_nodes(old_nodes)
