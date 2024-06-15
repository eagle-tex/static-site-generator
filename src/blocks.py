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
