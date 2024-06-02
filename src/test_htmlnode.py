import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
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
        self.assertEqual(
            html_node2.props_to_html(),
            ' href="https://www.google.com" target="_blank" alt="Link to Google"',
        )

    def test_repr1(self):
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
        repr = html_node1.__repr__()
        expected_output = """--------------------
HTMLNode
Tag: a
Value: My link
Child #1
    --------------------
    HTMLNode
    Tag: a1
    Value: Google
    Children: None
    Props: None
    --------------------
Child #2
    --------------------
    HTMLNode
    Tag: a2
    Value: Netflix
    Child #1
        --------------------
        HTMLNode
        Tag: a21
        Value: What's next?
        Children: None
        Props: {'src': 'image source', 'alt': 'a picture'}
        --------------------
    Props: None
    --------------------
Props: {'href': 'https://www.google.com', 'target': '_blank', 'alt': 'Link to Google'}
--------------------"""
        # print(html_node1)
        self.assertEqual(repr, expected_output)

    def test_repr2(self):
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
        repr = html_node2.__repr__()
        expected_output = """--------------------
HTMLNode
Tag: b
Value: My link
Children: None
Props: {'href': 'https://www.google.com', 'target': '_blank', 'alt': 'Link to Google'}
--------------------"""
        self.assertEqual(repr, expected_output)


if __name__ == "__main__":
    unittest.main()
