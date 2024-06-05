from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode
from htmlnode import HTMLNode


def main():
    print("running main.py")
    text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node)

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

    leafnode1 = LeafNode("p", "This is a paragraph of text.")
    leafnode2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(leafnode1)
    print(leafnode2)
    print(leafnode1.to_html())
    print(leafnode2.to_html())
    print()

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
