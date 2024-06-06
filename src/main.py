from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode
from htmlnode import HTMLNode


def main():
    print("running main.py")
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

    print("**************** LEAF NODES *******************")

    leafnode1 = LeafNode("p", "This is a paragraph of text.")
    leafnode2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(leafnode1)
    print(leafnode2)
    print(leafnode1.to_html())
    print(leafnode2.to_html())
    print()

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


main()
