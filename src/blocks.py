from typing import List
import re

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

block_type_code = "code"
block_type_heading = "heading"
block_type_ordered_list = "ordered_list"
block_type_paragraph = "paragraph"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"


def markdown_to_text(markdown: str) -> List[str]:
    """
    Separates a block of markdown text into blocks of different types
    Blocks are a group of lines without any empty line(s)

    Argument
    --------
    markdown: str
        a markdown text (multiline)

    Returns
    -------
    A list of blocks of different types
    The types of blocks are
        - code
        - heading
        - ordered_list
        - paragraph
        - quote
        - unordered list
    """
    blocks = []
    raw_lines = markdown.split("\n")
    print(f"markdown_to_text -> raw_lines = {raw_lines}")
    stripped_lines = list(map(lambda text: text.strip(), raw_lines))
    curr_block = []

    for i in range(0, len(stripped_lines)):
        content = stripped_lines[i]

    for i in range(0, len(stripped_lines)):
        content = stripped_lines[i]
        if content != "":
            if content.startswith(("- ", "* ", "+ ")) or bool(
                re.search(r"^(\d+)\. ", content)
            ):
                curr_block.append(raw_lines[i].rstrip())
            else:
                curr_block.append(stripped_lines[i])
        else:
            if len(curr_block) > 0:  # curr_block is not empty
                blocks.append("\n".join(curr_block))
                curr_block = []  # reset curr_block

    return blocks


def block_to_block_type(block: str) -> str:
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_unordered_list = "unordered_list"
    block_type_ordered_list = "ordered_list"

    if block == "":
        raise ValueError(f"<block> argument is an empty string -> Not allowed")

    # break the block into lines
    lines = block.split("\n")

    def is_heading(line):
        stripped_line = line.strip("#")
        if stripped_line != line:
            if stripped_line[0] == " " and stripped_line[1] != " ":
                return True
        return False

    new_lines = list(filter(is_heading, lines))
    if len(new_lines) == len(lines):
        return block_type_heading

    # Check for quote block
    new_lines = list(filter(lambda line: line.startswith(">"), lines))
    if len(new_lines) == len(lines):
        return block_type_quote

    # Check for list block (ordered or unordered)
    stripped_lines = list(map(lambda text: text.strip(), lines))
    if stripped_lines[0].startswith(("- ", "* ", "+ ")):
        is_ordered_list_el = False
        is_unordered_list_el = True
    elif bool(re.search(r"^(\d+)\. ", stripped_lines[0])):
        is_ordered_list_el = True
        is_unordered_list_el = False
    else:
        is_ordered_list_el = False
        is_unordered_list_el = False

    block_is_a_list = False
    for i in range(0, len(stripped_lines)):
        content = stripped_lines[i]
        if (content[0] in "-*+" and content[1] == " ") or bool(
            re.search(r"^(\d+)\. ", content)
        ):
            block_is_a_list = True
        else:
            block_is_a_list = False

    if block_is_a_list:
        if is_ordered_list_el:
            return block_type_ordered_list
        if is_unordered_list_el:
            return block_type_unordered_list

    # Check for code block
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return block_type_code

    # if all the other checks fail, then it's a paragraph block
    return block_type_paragraph


def code_block_to_html_node(block: str, type: str):
    nodes = []
    if type == "code":
        block_lines = block.split("\n")
        for bl in block_lines:
            if bl.startswith("```"):
                # do not add this line to the output
                continue
            elif bl.endswith("```"):
                if len(bl) > 3:
                    nodes.append(bl.rstrip("`"))
                else:
                    continue
            else:
                nodes.append(bl)
        nodes_as_text = "\n".join(nodes)
        html_node = HTMLNode("pre", None, [HTMLNode("code", nodes_as_text, None, None)])
        return html_node
    else:
        raise ValueError(f'Argument <type> different from "code"')


def heading_block_to_html_node(block: str, type: str):
    nodes = []
    if type == "heading":
        # split block into lines
        lines = block.split("\n")
        for line in lines:
            pass
            # count the number of "#" at the beginning
            num_hashes = 0
            for i in range(6):  # maximum 6 hashes allowed
                if line[i] == "#":
                    num_hashes += 1
                else:  # if line[i] != "#"
                    break
            tag = f"h{num_hashes}"
            curr_node = LeafNode(tag, line.lstrip("# "))
            nodes.append(curr_node)
        return nodes
    else:
        raise ValueError(f'Argument <type> different from "heading"')


def print_stack(stack):
    result = []
    for el in stack:
        result.append((el[0].tag, type(el[0]).__name__, el[1]))
    return result


def add_to_parent(node, stack, leading_spaces: int):
    parent_node = stack[-1][0]
    parent_node.children.append(node)
    stack.append((node, leading_spaces))


def list_to_html_node(block: str, type: str):
    if type not in [block_type_ordered_list, block_type_unordered_list]:
        raise ValueError(f'Argument <type> is not "ordered_list" or "unordered_list"')

    lines = block.split("\n")
    root = ParentNode("div", [])
    stack = [(root, -1)]  # Stack of tuples (node, indentation_level)

    spaces = []  # a list to store the number of leading spaces for each line
    element_has_children = (
        []
    )  # a list of booleans: True for each line that have nested element
    for i, line in enumerate(lines):
        leading_spaces = len(line) - len(line.lstrip())
        spaces.append(leading_spaces)
        element_has_children.append(False)  # fill array with False values

    for i in range(1, len(lines)):
        if spaces[i] > spaces[i - 1]:
            element_has_children[i - 1] = True

    for i, line in enumerate(lines):
        if not line.strip():
            continue  # skip empty lines

        leading_spaces = spaces[i]
        content = line.lstrip()

        list_type = ""
        # Determine the list item type and tag
        if content.startswith(("-", "*", "+")):
            # Unordered list item
            content = content[1:].lstrip()
            list_type = "ul"

        elif bool(re.search(r"^(\d+)\.", content)):
            # Ordered list item
            content = content.lstrip("0123456789.").lstrip(" ")
            list_type = "ol"

        if element_has_children[i]:
            item_node = ParentNode("li", [LeafNode(None, content)])
        else:
            item_node = LeafNode("li", content)

        while (
            stack
            and (
                stack[-1][1] >= leading_spaces and not stack[-1][0].tag in ["ul", "ol"]
            )
            or (stack[-1][1] > leading_spaces and stack[-1][0].tag in ["ul", "ol"])
        ):
            stack.pop()

        # Check if the current parent is not an unordered list
        # if not stack[-1][0].tag in ["ul", "ol"]:
        if stack[-1][0].tag not in ["ul", "ol"]:
            # print(f'Stack last item tag = "{stack[-1][0]}"')
            list_node = ParentNode(list_type, [])
            add_to_parent(list_node, stack, leading_spaces)
            add_to_parent(item_node, stack, leading_spaces)
        else:
            add_to_parent(item_node, stack, leading_spaces)

    return root


def ordered_list_to_html_node(block: str, type: str = "ordered_list"):
    li_nodes = []
    if type != "ordered_list":
        raise ValueError(f'Argument <type> is not "ordered_list"')

    lines = block.split("\n")
    for i in range(len(lines)):
        li_nodes.append(LeafNode("li", lines[i].lstrip(f"{i+1}. ")))

    parent_node = ParentNode("ol", li_nodes)
    return parent_node


def unordered_list_to_html_node(block: str, type: str = "unordered_list"):
    li_nodes = []
    if type == "unordered_list":
        lines = block.split("\n")
        for line in lines:
            li_nodes.append(LeafNode("li", line.lstrip("* ")))

        parent_node = ParentNode("ul", li_nodes)
        return parent_node
    else:
        raise ValueError(f'Argument <type> different from "unordered_list"')


def paragraph_block_to_html_node(content: str, type: str = "paragraph"):
    if type != "paragraph":
        raise ValueError(f'Argument <type> is not "paragraph"')

    node = LeafNode("p", content)
    return node


def quote_block_to_html_node(content: str, type: str = "quote"):
    nodes = []
    if type != "quote":
        raise ValueError(f'Argument <type> is not "quote"')

    lines = content.split("\n")
    for line in lines:
        nodes.append(LeafNode(None, f'{line.lstrip(">")}\n'))

    parent_node = ParentNode("blockquote", nodes)
    return parent_node


def markdown_to_html_node(markdown: str):
    children = []
    raw_text_blocks = markdown_to_text(markdown)

    for curr_block in raw_text_blocks:
        child_node = None
        block_type = block_to_block_type(curr_block)
        if block_type == block_type_code:
            child_node = code_block_to_html_node(curr_block, block_type_code)
        elif block_type == block_type_heading:
            # heading_block_to_html_node returns an array of heading LeafNodes
            children.extend(heading_block_to_html_node(curr_block, block_type_heading))
            continue  # move directly to next iteration
        elif block_type == block_type_ordered_list:
            child_node = ordered_list_to_html_node(curr_block, block_type_ordered_list)
        elif block_type == block_type_quote:
            child_node = quote_block_to_html_node(curr_block, block_type_quote)
        elif block_type == block_type_unordered_list:
            child_node = unordered_list_to_html_node(
                curr_block, block_type_unordered_list
            )
        else:
            child_node = paragraph_block_to_html_node(curr_block, block_type_paragraph)
        children.append(child_node)

    return ParentNode("div", children)

