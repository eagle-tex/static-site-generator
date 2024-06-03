from leafnode import LeafNode
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


main()
