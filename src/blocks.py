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
    stripped_lines = list(map(lambda text: text.strip(), raw_lines))
    curr_block = []
    is_ordered_list_el = True
    is_unordered_list_el = True
    for i in range(0, len(stripped_lines)):
        content = stripped_lines[i]
        if content != "":
            if content.startswith(("- ", "* ", "+ ")) and is_unordered_list_el:
                curr_block.append(raw_lines[i].rstrip())
                is_ordered_list_el = False
            elif bool(re.search(r"^(\d+)\. ", content)) and is_ordered_list_el:
                curr_block.append(raw_lines[i].rstrip())
                is_unordered_list_el = False
            else:
                curr_block.append(stripped_lines[i])
                is_ordered_list_el = False
                is_unordered_list_el = False
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

    # Check for unordered_list block
    new_lines = list(
        filter(lambda line: line.lstrip().startswith(("* ", "+ ", "- ")), lines)
    )
    if len(new_lines) == len(lines):
        return block_type_unordered_list

    # Check for code block
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return block_type_code

    # Check for ordered_list block
    new_lines = []
    is_match = False
    for i in range(len(lines)):
        if lines[i].lstrip().startswith(f"{i+1}. "):
            is_match = True
        else:
            is_match = False
            return block_type_paragraph
    if is_match:
        return block_type_ordered_list

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


# def parse_markdown(markdown:str):
#     lines=markdown.split("\n")
#     root=ParentNode("div",[])
#     stack=[(root,-1)] # Stack of tuples (node, indentation_level)
#
#     def add_to_parent(node):
#         nonlocal stack
#         while stack and stack[-1][1]>=leading_spaces:
#             stack.pop()
#         current_parent=stack[-1][0]
#         current_parent.children.append(node)


def print_stack(stack):
    result = []
    for el in stack:
        result.append(el[1])
    return result


def list_to_html_node(block: str, type: str):
    if type not in [block_type_ordered_list, block_type_unordered_list]:
        raise ValueError(f'Argument <type> is not "ordered_list" or "unordered_list"')

    lines = block.split("\n")
    print("---------------------------------")
    print(lines)
    print("---------------------------------")
    root = ParentNode("div", [])
    current_parent = root
    # stack= [(root, -1)]  # (node, indentation_level)
    stack: List[tuple[ParentNode | LeafNode, int]] = [
        (root, -1)
    ]  # Stack of tuples (node, indentation_level)

    for i, line in enumerate(lines):
        print(f"====== Iteration {i+1} ======")
        if not line.strip():
            continue  # skip empty lines

        leading_spaces = len(line) - len(line.lstrip())
        content = line.lstrip()
        print(f'Initial content: "{content}"')
        print(f"Leading spaces = {leading_spaces}")

        # Determine the list item type and tag
        if content.startswith(("-", "*", "+")):
            list_tag = "ul"
            item_tag = "li"
            content = content[2:].lstrip()
            print(f"Unord_List > Content: {content}")
        elif bool(re.search(r"^(\d+)\.", content)):
            list_tag = "ol"
            item_tag = "li"
            content = line.lstrip(f"{i+1}. ")
            print(f"Ord_List > Content: {content}")
        else:
            continue  # not a list item

        # Adjust the current parent based on indentation
        while stack and stack[-1][1] >= leading_spaces:
            print(f"popping a stack element at iteration {i+1}")
            stack.pop()
        current_parent = stack[-1][0]
        print(f"CP1 - current_parent.tag = {current_parent.tag}")

        # Create a new list if necessary
        if not current_parent.children or current_parent.children[-1].tag not in [
            "ul",
            "ol",
        ]:
            new_list = ParentNode(list_tag, [])
            if isinstance(current_parent.children, list):
                current_parent.children.append(new_list)
                print("passing inside if")
            current_parent = new_list
            stack.append((current_parent, leading_spaces))
            print(f"CP2 - current_parent.tag = {current_parent.tag}")
            # print(f"number of stack elements: {len(stack)}")
            print(f"stack repr: {print_stack(stack)}")

        # Add the list item to the current list
        new_item = LeafNode(item_tag, content)
        if isinstance(current_parent.children, list):
            current_parent.children.append(new_item)
            print(
                f'Inside 2nd if: Appended "{new_item.to_html()}" to <{current_parent.tag}> children'
            )
        stack.append((new_item, leading_spaces + 2))  # Set for potential children
        # print(f"number of stack elements: {len(stack)}")
        print(f"stack repr: {print_stack(stack)}")

        print(f"****** End of iteration {i+1} ******\n")

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


def paragraph_block_to_html_node(block: str, type: str = "paragraph"):
    if type != "paragraph":
        raise ValueError(f'Argument <type> is not "paragraph"')

    node = LeafNode("p", block)
    return node


def quote_block_to_html_node(block: str, type: str = "quote"):
    nodes = []
    if type != "quote":
        raise ValueError(f'Argument <type> is not "quote"')

    lines = block.split("\n")
    for line in lines:
        nodes.append(LeafNode(None, f'{line.lstrip(">")}\n'))

    parent_node = ParentNode("blockquote", nodes)
    return parent_node


def markdown_to_html_node(markdown: str):
    children = []
    raw_text_blocks = markdown_to_text(markdown)
    # print("------- Raw Text Blocks -------")
    # for rtb in raw_text_blocks:
    #     print(rtb)
    # print()

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
