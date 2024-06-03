import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_success(self):
        leafnode1 = LeafNode("p", "This is a paragraph of text.")
        expected1 = "<p>This is a paragraph of text.</p>"
        leafnode2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leafnode1.to_html(), expected1)
        self.assertEqual(leafnode2.to_html(), expected2)

    def test_to_html_tag(self):
        leafnode1 = LeafNode(None, "This is a leafnode with no value.")
        self.assertEqual(leafnode1.to_html(), leafnode1.value)

    def test_to_html_value(self):
        with self.assertRaises(ValueError):
            leafnode1 = LeafNode("p", None)
            leafnode1.to_html()
