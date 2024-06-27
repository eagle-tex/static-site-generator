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
                HTMLNode("SEARCH", "Google"),
                HTMLNode(
                    "DUMMY",
                    "Netflix",
                    children=[
                        HTMLNode(
                            "IMAGINARY",
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
        expected_output = """<a href="https://www.google.com" target="_blank" alt="Link to Google">
  My link
  <SEARCH>Google</SEARCH>
  <DUMMY>
    Netflix
    <IMAGINARY src="image source" alt="a picture">What's next?</IMAGINARY>
  </DUMMY>
</a>"""
        # print(html_node1)
        self.assertEqual(repr, expected_output)

    def test_repr2(self):
        html_node2 = HTMLNode(
            "link_tag",
            "My link",
            children=None,
            props={
                "href": "https://www.google.com",
                "target": "_blank",
                "alt": "Link to Google",
            },
        )
        repr = html_node2.__repr__()
        expected_output = """<link_tag href="https://www.google.com" target="_blank" alt="Link to Google">
  My link
</link_tag>"""
        self.assertEqual(repr, expected_output)


if __name__ == "__main__":
    unittest.main()
