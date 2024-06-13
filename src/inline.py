import re
from typing import List, Tuple
from textnode import TextNode


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


def extract_markdown_images(text: str) -> List[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text: str) -> List[tuple[str, str]]:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
