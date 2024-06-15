from typing import List


def markdown_to_text(markdown: str) -> List[str]:
    blocks = []
    raw_splits = markdown.split("\n")
    stripped_splits = list(map(lambda text: text.strip(), raw_splits))
    # blocks = list(filter(lambda text: text != "", splits))
    curr_block = []
    for i in range(0, len(stripped_splits)):
        if stripped_splits[i] != "":
            curr_block.append(stripped_splits[i])
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
        filter(lambda line: line.startswith("* ") or line.startswith("- "), lines)
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
        if lines[i].startswith(f"{i+1}. "):
            is_match = True
        else:
            is_match = False
            return block_type_paragraph
    if is_match:
        return block_type_ordered_list

    # if all the other checks fail, then it's a paragraph block
    return block_type_paragraph
