from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, split_nodes_delimiter
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
        props={
            "href": "https://www.google.com",
            "target": "_blank",
            "alt": "Link to Google",
        },
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
    text_type_bold = "bold"
    text_type_code = "code"
    text_type_italic = "italic"
    node1 = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes1 = split_nodes_delimiter([node1], "`", text_type_code)
    for node in new_nodes1:
        print(f'Content: "{node.text}", Type: {node.text_type}')
    # print(new_nodes1)


def main():
    print("running main.py")
    # play_with_text_nodes()
    # play_with_html_nodes()
    # play_with_leaf_nodes()
    # play_with_parent_nodes()
    play_with_split_delimiter()


main()
