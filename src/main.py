from textnode import TextNode
from htmlnode import HTMLNode


def main():
    print("running main.py")
    text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node)

    html_node1 = HTMLNode(
        "a",
        "My link",
        children=[
            HTMLNode("a1", "Google"),
            HTMLNode(
                "a2",
                "Netflix",
                children=[
                    HTMLNode(
                        "a21",
                        "What's next?",
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
        "b",
        "My link",
        children=None,
        props={
            "href": "https://www.google.com",
            "target": "_blank",
            "alt": "Link to Google",
        },
    )
    print(html_node2)


main()
