import os
from os.path import isfile
from typing import List

from blocks import markdown_to_html_node
from copy_static import check_dest_dir, check_if_file_exists, validate_src_dir


def extract_title(markdown: str) -> str:
    lines: List[str] = markdown.split("\n")

    for line in lines:
        stripped_line = line.strip(" ")
        if stripped_line.startswith("# "):
            h1_line: str = stripped_line
            h1_header: str = h1_line.lstrip("# ")
            return h1_header

    raise Exception("There is no H1 header in the input")


def generate_page(from_path: str, template_path: str, dest_path: str):
    check_if_file_exists(from_path)
    check_if_file_exists(template_path)

    # read 'from_path' file
    markdown = ""
    with open(from_path) as input_file:
        markdown = input_file.read()
        # print(f"from_path: {from_path}\ncontent: {markdown}\n")

    # read 'template_path' file
    html_template = ""
    with open(template_path) as template_file:
        html_template = template_file.read()

    html_node = markdown_to_html_node(markdown)
    md_to_html_content = html_node.to_html()
    # print(f"markdown_to_html_content: \n{md_to_html_content}")

    # extract the title of the page from the markdown
    h1_title = extract_title(markdown)
    # print(f"h1_title: {h1_title}")

    # replace {{ Title }} and {{ Content }} in the template
    final_html = html_template.replace("{{ Title }}", h1_title).replace(
        "{{ Content }}", md_to_html_content
    )
    print(f"final_html: {final_html}")

    # write the new full HTML to 'dest_file'
    if not os.path.exists(dest_path):
        path_tokens = dest_path.split("/")
        # file_name = path_tokens[-1]
        if len(path_tokens) > 1:
            dirs_path = "/".join(path_tokens[:-1])
            os.makedirs(dirs_path, exist_ok=True)

    print(
        f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'"
    )
    with open(dest_path, "w") as f:
        f.write(final_html)


def is_markdown_file(file_path: str) -> bool:
    return file_path.endswith(".md")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> None:
    validate_src_dir(dir_path_content)
    check_if_file_exists(template_path)
    # check_dest_dir(dest_dir_path)

    for entry in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, entry)
        if os.path.isfile(src_item) and is_markdown_file(src_item):
            src_file = src_item
            dest_path = src_file.replace(dir_path_content, dest_dir_path).replace(
                ".md", ".html"
            )
            generate_page(src_item, template_path, dest_path)
        elif os.path.isdir(src_item):
            src_dir = src_item
            dest_dir = src_dir.replace(dir_path_content, dest_dir_path)
            os.makedirs(dest_dir, exist_ok=True)
            generate_pages_recursive(src_dir, template_path, dest_dir)


if __name__ == "__main__":
    output = extract_title("# Hello")
    print(output)

    output = extract_title("  # Hello World  ")
    print(output)

    generate_page("content/index.md", "template.html", "tata/index.html")
