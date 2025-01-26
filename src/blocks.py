from typing import List, Tuple
import re

from inline import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode

block_type_code = "code"
block_type_heading = "heading"
block_type_ordered_list = "ordered_list"
block_type_paragraph = "paragraph"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
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
    code_block_active = False

    for i in range(0, len(stripped_lines)):
        content = stripped_lines[i]
        if content != "":
            if content.startswith(("- ", "* ", "+ ")) or bool(
                re.search(r"^(\d+)\. ", content)
            ):  # list (unordered or ordered)
                curr_block.append(raw_lines[i].rstrip())
            elif content.startswith("#") and not code_block_active:  # heading
                curr_block.append(content.strip())
            elif content.startswith("> "):  # blockquote
                curr_block.append(content.strip())
            elif content.startswith("```") and not code_block_active:
                code_block_active = True
                curr_block.append(
                    raw_lines[i].rstrip()
                )  # add line with beginning whitespace
            elif content.endswith("```") and code_block_active:
                curr_block.append(
                    raw_lines[i].rstrip()
                )  # add line with beginning whitespace
                code_block_active = False
            elif code_block_active:
                curr_block.append(raw_lines[i].rstrip())
            else:
                curr_block.append(content)

            if i == len(stripped_lines) - 1:  # last line
                blocks.append("\n".join(curr_block))
        else:
            if len(curr_block) > 0:  # curr_block is not empty
                blocks.append("\n".join(curr_block))
                curr_block = []  # reset curr_block

    return blocks


def is_heading(line: str) -> bool:
    """
    Checks if a line (string) is a Markdown heading

    Argument
    --------
    line: str
        a Markdown text (one line)

    Returns
    -------
    True if the line is a Markdown heading
    False otherwise
    """
    left_stripped_line = line.lstrip("#")
    if left_stripped_line.rstrip() != line.rstrip():
        if left_stripped_line[0] == " " and left_stripped_line[1] != " ":
            return True
    return False


def block_to_block_type(block: str) -> str:
    """
    Gets a block (a set of non-empty lines) and returns
    the corresponding block type

    Argument
    --------
    block: str
        a set (1 or more) of non-empty lines

    Returns
    -------
    The block type: str
    The available/possible block types are:
        - code
        - heading
        - ordered_list
        - paragraph
        - quote
        - unordered_list
    """
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
        if content:
            if (content[0] in "-*+" and content[1] == " ") or bool(
                re.search(r"^(\d+)\. ", content)
            ):
                block_is_a_list = True
            else:
                block_is_a_list = False
        else:
            continue

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


def code_block_to_html_node(block: str, type: str) -> ParentNode:
    """
    Transforms a Mardown code block into an HTML node

    Argument
    --------
    1. block (str): a multiline string
    2. [type (str)]: optional. can only take value "code", which it defaults to if omitted


    Returns
    -------
    A HTML element of type `ParentNode`
        A div element as root node, with a <pre> element inside
        and a <code> element inside the <pre> element

    Raises
    ------
    ValueError: when `type` is not `"code"`

    Example
    -------
    <div>
        <pre>
            <code>
            code line 1
            code line 2
            ...
            code line n
            </code>
        </pre>
    </div>
    """
    nodes = []
    if type == "code":
        block_lines = block.split("\n")
        for block_line in block_lines:
            if block_line.startswith("```"):
                # do not add this line to the output
                continue
            elif block_line.endswith("```"):
                if len(block_line) > 3:
                    nodes.append(block_line.rstrip("`"))
                else:
                    continue
            else:
                nodes.append(block_line)
        nodes_as_text = "\n".join(nodes)
        html_node = ParentNode("pre", [LeafNode("code", nodes_as_text, None)])
        return html_node
    else:
        raise ValueError(f'Argument <type> different from "code"')


def heading_block_to_html_node(block: str, type: str):
    """
    Transforms a Mardown `heading` block into an HTML node

    Argument
    --------
    1. block (str): a multiline string
    2. [type (str)]: optional. can only take value `"heading"`, which it defaults to if omitted


    Returns
    -------
    A HTML element of type `ParentNode`
        A div element as root node, with one or multiplie heading element inside
        Heading elements are h1, h2 ... to h6

    Raises
    ------
    ValueError: when `type` is not `"heading"`

    Example
    -------
    <div>
        <h1>Heading level 1</h1>
        <h2>Heading level 2</h2>
        ...
    </div>
    """
    nodes = []
    if type == "heading":
        # split block into lines
        lines = block.split("\n")
        for line in lines:
            pass
            # count the number of "#" at the beginning
            num_hashes = 0
            for i in range(6):  # maximum 6 hashes allowed
                if line[i].lstrip() == "#":
                    num_hashes += 1
                else:  # if line[i] != "#"
                    break
            tag = f"h{num_hashes}"
            curr_node = LeafNode(tag, line.rstrip().lstrip("# "))
            nodes.append(curr_node)
        return nodes
    else:
        raise ValueError(f'Argument <type> different from "heading"')


def stack_repr(
    stack: List[tuple[LeafNode | ParentNode, int]]
) -> List[Tuple[str, str, int]]:
    """
    Helper function for debugging
    Prints a stack of tuples

    Argument
    --------
    stack: a list of `(Tuple[LeafNode | ParentNode, int])` elements

    Returns
    -------
    An array of `(element_tag: str, element_name: str, leading_spaces: int)`
            where:
                - element is of type `LeafNode` or `ParentNode`
                - leading_spaces is the number of spaces (i.e the nesting level)
    """
    result = []
    for el in stack:
        result.append((el[0].tag, type(el[0]).__name__, el[1]))
    return result


def clean_stack(stack, leading_spaces):
    """
    Helper function
    Removes all elements up to but not including the direct parent of the current element in a list
    i.e.
    Removes `LeafNode` elements from stack
        - `LeafNode` elements which leading_spaces are >= to the current `leading_spaces` value
        - List `ParentNode` (`ul` or `ol`) which leading_spaces are > to the current `leading_spaces` value
    """
    while (
        stack
        and (stack[-1][1] >= leading_spaces and not stack[-1][0].tag in ["ul", "ol"])
        or (stack[-1][1] > leading_spaces and stack[-1][0].tag in ["ul", "ol"])
    ):
        stack.pop()


def add_to_parent(node, stack, leading_spaces: int):
    # TODO: add docstring
    parent_node = stack[-1][0]
    if isinstance(parent_node, ParentNode) and isinstance(parent_node.children, list):
        parent_node.children.append(node)
    stack.append((node, leading_spaces))


def list_to_html_node(block: str, type: str):
    # TODO: add docstring
    if type not in [block_type_ordered_list, block_type_unordered_list]:
        raise ValueError(f'Argument <type> is not "ordered_list" or "unordered_list"')

    lines = block.split("\n")
    root = ParentNode("div", [])
    stack = [(root, -1)]  # Stack of tuples (node, indentation_level)

    spaces = []  # a list to store the number of leading spaces for each line
    # A list of booleans: True for each line that have a nested element
    element_has_children = []
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
        if content.startswith(("- ", "* ", "+ ")):
            # Unordered list item
            content = content[1:].lstrip()
            list_type = "ul"

        elif bool(re.search(r"^(\d+)\.", content)):
            # Ordered list item
            content = content.lstrip("0123456789.").lstrip(" ")
            list_type = "ol"

        text_nodes = text_to_textnodes(content)
        html_nodes = []
        for text_node in text_nodes:
            html_nodes.append(text_node.text_node_to_html_node())

        if element_has_children[i]:
            # Create a list node (<li>) that contains all the html nodes
            item_node = ParentNode("li", html_nodes)
        else:
            html_str = ""
            for node in html_nodes:
                html_str += node.to_html()
            item_node = LeafNode("li", html_str)

        while (
            stack
            and (
                stack[-1][1] >= leading_spaces and not stack[-1][0].tag in ["ul", "ol"]
            )
            or (stack[-1][1] > leading_spaces and stack[-1][0].tag in ["ul", "ol"])
        ):
            stack.pop()

        # Check if the current parent is not a ordered list
        if stack[-1][0].tag not in ["ul", "ol"]:
            # print(f'Stack last item tag = "{stack[-1][0]}"')
            list_node = ParentNode(list_type, [])
            add_to_parent(list_node, stack, leading_spaces)
            add_to_parent(item_node, stack, leading_spaces)
        else:
            add_to_parent(item_node, stack, leading_spaces)

    return root


def ordered_list_to_html_node(block: str, type: str = "ordered_list"):
    # TODO: add docstring
    li_nodes = []
    if type != "ordered_list":
        raise ValueError(f'Argument <type> is not "ordered_list"')

    lines = block.split("\n")
    for i in range(len(lines)):
        li_nodes.append(LeafNode("li", lines[i].lstrip(f"{i+1}. ")))

    parent_node = ParentNode("ol", li_nodes)
    return parent_node


def unordered_list_to_html_node(block: str, type: str = "unordered_list"):
    # TODO: add docstring
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
    # TODO: add docstring
    if type != "paragraph":
        raise ValueError(f'Argument <type> is not "paragraph"')

    node = LeafNode("p", content.strip())
    return node


def quote_block_to_html_node(content: str, type: str = "quote"):
    # TODO: add docstring
    nodes = []
    if type != "quote":
        raise ValueError(f'Argument <type> is not "quote"')

    lines = content.split("\n")
    for line in lines:
        nodes.append(LeafNode(None, f'{line.lstrip("> ")}'))

    parent_node = ParentNode("blockquote", nodes)
    return parent_node


def parse_markdown(markdown):
    # TODO: add docstring
    lines = markdown.split("\n")
    root = ParentNode("div", [])
    stack = [(root, -1)]

    spaces = []  # a list to store the number of leading spaces for each line
    # A list of booleans: True for each line that have a nested element
    element_has_children = []
    for i, line in enumerate(lines):
        leading_spaces = len(line) - len(line.lstrip())
        spaces.append(leading_spaces)
        element_has_children.append(False)  # fill array with False values

    for i in range(1, len(lines)):
        if spaces[i] > spaces[i - 1]:
            element_has_children[i - 1] = True

    code_block_active = False
    code_block_content = []
    code_block_lines_leading_spaces = []

    for i, line in enumerate(lines):
        content = line.strip()
        leading_spaces = spaces[i]

        if content.startswith("```"):
            if code_block_active:
                # End of code block
                code_node = ParentNode(
                    "pre", [LeafNode("code", "\n".join(code_block_content))]
                )
                add_to_parent(code_node, stack, leading_spaces)
                code_block_active = False
                code_block_content = []
                # number of leading spaces on chaque line in a code block
                code_block_lines_leading_spaces = []
            else:
                # Start of code block
                code_block_active = True
                # element_has_children[i + 1] = False
                code_block_content = []
                code_block_lines_leading_spaces = []
            continue

        if code_block_active:
            # Append the line with all its leading spaces
            # TODO: add comments to explain these variables
            code_block_lines_leading_spaces.append(leading_spaces)
            num_of_elements_in_code_block = len(code_block_lines_leading_spaces)
            number_of_spaces = (
                code_block_lines_leading_spaces[num_of_elements_in_code_block - 1]
                - code_block_lines_leading_spaces[0]
            )
            code_line_padding = number_of_spaces * " "
            code_block_content.append(code_line_padding + content)
            continue

        if content.startswith(">"):
            blockquote_content = content[1:].strip()
            # Convert the content to text nodes and process inline markdown
            text_nodes = text_to_textnodes(blockquote_content)
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node.text_node_to_html_node())

            # Combine the html nodes into a single string
            html_str = ""
            for node in html_nodes:
                html_str += node.to_html()

            # Create the blockquote node with the processed content
            blockquote_node = ParentNode(
                "blockquote", [LeafNode(None, html_str.strip())]
            )
            # print("Debug - blockquote HTML:", blockquote_node.to_html())
            add_to_parent(blockquote_node, stack, leading_spaces)

        elif content.startswith("#"):
            hash_count = content.count("#", 0, content.index(" "))
            heading_content = content[hash_count:].strip()
            heading_node = LeafNode(f"h{hash_count}", heading_content)
            clean_stack(stack, leading_spaces)
            add_to_parent(heading_node, stack, leading_spaces)

        elif (content.startswith(("- ", "* ", "+ "))) or bool(
            re.search(r"^(\d+)\. ", content)
        ):
            list_type = ""
            # Determine the list item type and tag
            if content.startswith(("- ", "* ", "+ ")):
                # Unordered list item
                content = content[1:].lstrip()
                list_type = "ul"

            elif bool(re.search(r"^(\d+)\.", content)):
                # Ordered list item
                content = content.lstrip("0123456789.").lstrip(" ")
                list_type = "ol"

            text_nodes = text_to_textnodes(content)
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node.text_node_to_html_node())

            if element_has_children[i]:
                # Create a list node (<li>) that contains all the html nodes
                item_node = ParentNode("li", html_nodes)
            else:
                html_str = ""
                for node in html_nodes:
                    html_str += node.to_html()
                item_node = LeafNode("li", html_str)

            clean_stack(stack, leading_spaces)

            # Check if the current parent is not a list, unordered or ordered
            if stack[-1][0].tag not in ["ul", "ol"]:
                list_node = ParentNode(list_type, [])
                add_to_parent(list_node, stack, leading_spaces)
                add_to_parent(item_node, stack, leading_spaces)
            else:
                add_to_parent(item_node, stack, leading_spaces)

        else:
            if content:
                # Process the content for inline elements
                text_nodes = text_to_textnodes(content)
                html_nodes = []
                for tn in text_nodes:
                    html_nodes.append(tn.text_node_to_html_node())
                # Create a paragraph node that contains all the html nodes
                paragraph_node = ParentNode("p", html_nodes)
                clean_stack(stack, leading_spaces)
                add_to_parent(paragraph_node, stack, leading_spaces)

    return root


def markdown_to_html_node(markdown: str):
    # TODO: add docstring
    children = []
    raw_text_blocks = markdown_to_blocks(markdown)

    for curr_block in raw_text_blocks:
        current_node = parse_markdown(curr_block)
        if (
            isinstance(current_node, ParentNode)
            and isinstance(current_node.children, list)
            and len(current_node.children) > 0
        ):
            children.extend(current_node.children)

    return ParentNode("div", children)
