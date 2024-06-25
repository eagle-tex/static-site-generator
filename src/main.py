from blocks import (
    list_to_html_node,
    markdown_to_html_node,
    paragraph_block_to_html_node,
    quote_block_to_html_node,
    block_to_block_type,
    code_block_to_html_node,
    heading_block_to_html_node,
    markdown_to_text,
    ordered_list_to_html_node,
    unordered_list_to_html_node,
)
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode
from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from htmlnode import HTMLNode


def play_with_text_nodes():
    print("**************** TEXT NODES *******************")
    text_node = TextNode("This is a TEXT text node", "text")
    print(text_node.text_node_to_html_node().to_html())
    bold_text_node = TextNode("This is a BOLD text node", "bold")
    print(bold_text_node.text_node_to_html_node().to_html())
    italic_text_node = TextNode("This is a ITALIC text node", "italic")
    print(italic_text_node.text_node_to_html_node().to_html())
    code_text_node = TextNode("This is a CODE text node", "code")
    print(code_text_node.text_node_to_html_node().to_html())
    link_text_node = TextNode(
        "This is a LINK text node", "link", "https://www.boot.dev"
    )
    print(link_text_node.text_node_to_html_node().to_html())
    img_text_node = TextNode(
        "This is a IMAGE text node", "image", "/assets/background1.jpg"
    )
    print(img_text_node.text_node_to_html_node().to_html())
    # pdf_text_node = TextNode("This is a PDF text node", "pdf")
    # print(pdf_text_node.text_node_to_html_node())
    print()


def play_with_html_nodes():
    print("**************** HTML NODES *******************")
    html_node1 = HTMLNode(
        "div",
        "My link",
        children=[
            HTMLNode("h2", "Google"),
            HTMLNode(
                "div",
                "Netflix",
                children=[
                    HTMLNode(
                        "img",
                        None,
                        children=None,
                        props={"src": "image source", "alt": "a picture"},
                    )
                ],
            ),
        ],
        # props={
        #     "href": "https://www.google.com",
        #     "target": "_blank",
        #     "alt": "Link to Google",
        # },
    )
    print(html_node1)
    print()

    html_node2 = HTMLNode(
        "a",
        "My link",
        children=None,
        props={
            "href": "https://www.google.com",
            "target": "_blank",
            "alt": "Link to Google",
        },
    )
    print(html_node2)
    print()


def play_with_leaf_nodes():
    print("**************** LEAF NODES *******************")

    leafnode1 = LeafNode("p", "This is a paragraph of text.")
    leafnode2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(leafnode1)
    print(leafnode2)
    print(leafnode1.to_html())
    print(leafnode2.to_html())
    print()


def play_with_parent_nodes():
    print("**************** PARENT NODES *******************")

    parent_node1 = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print(parent_node1.to_html())

    parent_node2 = ParentNode(
        "div",
        [
            ParentNode(
                "div",
                [
                    ParentNode(
                        "ul",
                        [
                            LeafNode("li", "Hyper Focus"),
                            LeafNode("li", "Deep Work"),
                            LeafNode("li", "Ultra Learning"),
                        ],
                    )
                ],
            ),
            LeafNode("span", "Colored text"),
            LeafNode(None, "Ordinary text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print(parent_node2.to_html())
    print()

    nested_node = ParentNode(
        "div",
        [
            ParentNode(
                "p",
                [
                    LeafNode("b", "Bold inside inner paragraph"),
                    LeafNode(None, "Normal inside inner paragraph"),
                ],
            ),
            LeafNode(None, "Normal text inside outer div"),
        ],
    )
    print(nested_node.to_html())
    print()

    one_child_node = ParentNode(
        "ul",
        [
            ParentNode(
                "li",
                [
                    LeafNode(None, "Single list item"),
                ],
            ),
        ],
    )
    print(one_child_node.to_html())


def play_with_split_delimiter():
    text_type_text = "text"
    # text_type_bold = "bold"
    text_type_code = "code"
    # text_type_italic = "italic"
    node1 = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes1 = split_nodes_delimiter([node1], "`", text_type_code)
    for node in new_nodes1:
        print(f'Content: "{node.text}", Type: {node.text_type}')
    # print(new_nodes1)


def play_with_extract_md_img():
    text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    print(extract_markdown_images(text))


def play_with_extract_md_links():
    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    print(extract_markdown_links(text))


def play_with_split_nodes_image():
    node1 = TextNode(
        "This is text with an ![first image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
        "text",
    )

    node2 = TextNode(
        "![third image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3idvOCJ.png) and another ![fourth image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/4unPdYb.png)",
        "text",
    )

    node3 = TextNode(
        "![fifth image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/5llwMBT.png)",
        "text",
    )

    node4 = TextNode("Only text", "text")

    # node1 = TextNode(
    #     " and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
    #     "text",
    # )

    # new_nodes = split_nodes_image([node1, node2, node3, node4])
    # new_nodes = split_nodes_image([node3])
    # print(f"{len(new_nodes)} nodes returned")
    # for n in new_nodes:
    #     print(n)

    nodes = [
        TextNode("No images here", "text"),  # No images
        TextNode("Start with ![image1](link1) text", "text"),  # Image at the start
        TextNode(
            "Middle text with ![image2](link2) inside", "text"
        ),  # Image in the middle
        TextNode("End text ![image3](link3)", "text"),  # Image at the end
        TextNode("![image](link)", "text"),
        TextNode("![image1](link1)![image2](link2)", "text"),
        TextNode(
            "Multiple ![image4](link4) images ![image5](link5) here", "text"
        ),  # Multiple images
    ]
    for node in nodes:
        print(split_nodes_image([node]))


def play_with_split_nodes_link():
    node1 = TextNode(
        "This is text with a [first link](https://www.example.com) and [another](https://www.example.com/another)",
        "text",
    )
    node2 = TextNode(
        "This is text with only [one link](https://www.example.com)",
        "text",
    )
    node3 = TextNode(
        "[only the link](https://www.example.com)",
        "text",
    )
    new_nodes1 = split_nodes_link([node3])
    print(f"{len(new_nodes1)} link node(s) came through!")
    for n in new_nodes1:
        print(n)


def play_with_text_to_textnodes():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    for node in new_nodes:
        print(node)


def play_with_markdown_to_text():
    markdown = """
# This is a heading       
## This is a sub-heading


         This is a paragraph of text.
    It has some **bold** and *italic* words inside of it.
      

* This is a list item
* This is second list item    
* This is third list item    
       
    """
    print(f"{len(markdown_to_text(markdown))} block(s) found")
    for el in markdown_to_text(markdown):
        print(f'"{el}"')
        print()


def play_with_block_types():
    blocks = [
        "# Heading\n## Sub-heading",
        ">a quote block\n>second quote\n>third quote",
        "* element 1\n* element 2\n* element 3",
        "```py\nprint('hello')\n```",
        "1. element 1\n2. element 2\n3. element 3",
        "# Heading\n##Sub-heading",
        ">a quote block\nsecond quote\n>third quote",
        "*element 1\n* element 2\n* element 3",
        "```py\nprint('hello')\n``",
        "1. element 1\n2. element 2\n4. element 3",
    ]
    for block in blocks:
        print("------------------------------")
        print(block)
        print(f"Block type: {block_to_block_type(block)}")


def play_with_code_block_to_html_node():
    code_block = "```py\n# comment\nnumber = 5\nprint(f'{number}')\n```"
    result = code_block_to_html_node(code_block, "code")
    print(result)


def play_with_heading_block_to_html_node():
    heading_block = "# Heading level 1\n## Heading level 2\n### Heading level 3"
    block_type = block_to_block_type(heading_block)
    result = heading_block_to_html_node(heading_block, block_type)
    for node in result:
        print(node.to_html())


def play_with_unordered_list_to_html_node():
    print("------ Function `play_unordered_list_to_html() ------")
    list_block = """* item 1
* item 2
  * item 2.1
  * item 2.2
    - item 2.2.1
    * item 2.2.2
  * item 2.3
  * item 2.4
    + item 2.4.1
    + item 2.4.2
* item 3"""
    block_type = block_to_block_type(list_block)
    print(list_block)
    print(block_type)
    result = list_to_html_node(list_block, block_type)
    print(result)
    print("*****************************************************\n")
    # print(result.to_html())


def play_with_ordered_list_to_html_node():
    print("------ Function `play_ordered_list_to_html() ------")
    list_block = """1. item 1 ordered
2. item 2 ordered
  1. item 2.1 ordered
  2. item 2.2 ordered
    1. item 2.2.1 ordered
    2. item 2.2.2 ordered
  3. item 2.3 ordered
  4. item 2.4 ordered
    1. item 2.4.1 ordered
    2. item 2.4.2 ordered
3. item 3 ordered"""
    block_type = block_to_block_type(list_block)
    print(list_block)
    print(block_type)
    result = list_to_html_node(list_block, block_type)
    print(result)
    print("*****************************************************\n")
    # print(result.to_html())


def play_with_mixed_list_to_html_node():
    print("------ Function `play_with_mixed_list_to_html() ------")
    list_block = """* item 1
* item 2
  * item 2.1
  * item 2.2
    * item 2.2.1
    * item 2.2.2
  * item 2.3
  * item 2.4
    1. item 2.4.1 ordered
    2. item 2.4.2 ordered
* item 3"""
    block_type = block_to_block_type(list_block)
    print(list_block)
    print(block_type)
    result = list_to_html_node(list_block, block_type)
    print(result)
    print("*****************************************************\n")
    # print(result.to_html())


def play_with_quote_block_to_html_node():
    quote_block = ">quote line 1\n>quote line 2\n>quote line 3"
    block_type = block_to_block_type(quote_block)
    result = quote_block_to_html_node(quote_block, block_type)
    print(result.to_html())


def play_with_paragraph_block_to_html_node():
    parag_block = "First line of paragraph\nSecond line\nAnd third line"
    block_type = block_to_block_type(parag_block)
    result = paragraph_block_to_html_node(parag_block, block_type)
    print(result.to_html())


def play_with_markdown_to_html_node():
    markdown = """
# This is a heading       
## This is a sub-heading


         This is a paragraph of text.
    It has some **bold** and *italic* words inside of it.
      

* This is one list item
* This is another list item    
* This is yet another list item    

1. This is list item #1 
2. This is list item #2  
3. This is list item #3    
       
    """
    result = markdown_to_html_node(markdown)
    print(result.to_html())


def main():
    # print("running main.py")
    # play_with_text_nodes()
    # play_with_html_nodes()
    # play_with_leaf_nodes()
    # play_with_parent_nodes()
    # play_with_split_delimiter()
    # play_with_extract_md_img()
    # print()
    # play_with_extract_md_links()
    # print()
    # play_with_split_nodes_image()
    # print()
    # play_with_split_nodes_link()
    # print()
    # play_with_text_to_textnodes()
    # play_with_markdown_to_text()
    # play_with_block_types()
    # play_with_code_block_to_html_node()
    # play_with_heading_block_to_html_node()
    play_with_unordered_list_to_html_node()
    play_with_ordered_list_to_html_node()
    play_with_mixed_list_to_html_node()
    # play_with_quote_block_to_html_node()
    # play_with_paragraph_block_to_html_node()
    # play_with_markdown_to_html_node()


main()
