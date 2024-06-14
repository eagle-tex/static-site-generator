import re
from typing import List
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


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    # loop through old_nodes
    for node in old_nodes:
        # extract all the images from the current <node> as tuples
        image_tuples = extract_markdown_images(node.text)
        length = len(image_tuples)

        # if no image found, just return the node as is
        if length == 0:
            new_nodes.append(node)
            continue

        index = 0
        curr_img_tup = image_tuples[index]
        curr_splits = node.text.split(f"![{curr_img_tup[0]}]({curr_img_tup[1]})", 1)

        if len(curr_splits) != 2:
            raise Exception("current split results in more than 2 elements")

        # create a TextNode of type "image"
        curr_img_as_text_node = TextNode(curr_img_tup[0], "image", curr_img_tup[1])

        # if curr_splits has exactly 2 elements
        for i, split in enumerate(curr_splits):  # i is either 0 or 1
            if i == 0:
                # the split is at the very beginning, i.e no text before it
                if split != "":  # if there is text before the split
                    # create a TextNode of type text and append it to new_nodes
                    new_nodes.append(TextNode(split, "text"))
                # either way i.e split=="" or split !=""
                # append the created TextNode of type "image"
                new_nodes.append(curr_img_as_text_node)
            else:  # i == 1
                # the split is at the very end and no text after it
                if split != "":
                    if index < length:  # if there is another image to be parsed
                        index += 1
                        new_nodes.extend(split_nodes_image([TextNode(split, "text")]))

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    # loop through the nodes: <old_nodes>
    for node in old_nodes:
        # extract all the links from the current <node> as tuples
        link_tuples = extract_markdown_links(node.text)
        length = len(link_tuples)

        # if no link found, just return the node as is
        if length == 0:
            new_nodes.append(node)
            continue  # go on to the next node in <old_nodes>

        index = 0
        curr_link_tup = link_tuples[index]
        curr_splits = node.text.split(f"[{curr_link_tup[0]}]({curr_link_tup[1]})", 1)

        if len(curr_splits) != 2:
            raise Exception(
                "The current split results in more than 2 elements - Check it!"
            )

        # create a TextNode of type "link"
        curr_link_as_text_node = TextNode(curr_link_tup[0], "link", curr_link_tup[1])

        # if <curr_splits> has exactly 2 elements
        for i, split in enumerate(curr_splits):  # i is either 0 or 1
            if i == 0:
                # the split is at the very beginning, i.e no text before it
                if split != "":  # if there is some text before the split
                    # create a TextNode of type text with the split and append it to new_nodes
                    new_nodes.append(TextNode(split, "text"))
                # if split=="" or split!="", append the created TextNode of type "image"
                new_nodes.append(curr_link_as_text_node)
            else:  # i == 1
                # the split is at the very end and has no text after it
                if split != "":
                    if index < length:  # if there is another link to be parsed
                        index += 1
                        new_nodes.extend(split_nodes_link([TextNode(split, "text")]))

    return new_nodes
