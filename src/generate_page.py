from typing import List


def extract_title(markdown: str) -> str:
    lines: List[str] = markdown.split("\n")

    for line in lines:
        stripped_line = line.strip(" ")
        if stripped_line.startswith("# "):
            h1_line: str = stripped_line
            h1_header: str = h1_line.lstrip("# ")
            return h1_header

    raise Exception("There is no H1 header in the input")


if __name__ == "__main__":
    output = extract_title("# Hello")
    print(output)

    output = extract_title("  # Hello World  ")
    print(output)
