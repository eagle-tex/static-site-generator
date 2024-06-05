import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class Test_ParentNode(unittest.TestCase):
    def test_parentnode1_to_html(self):
        parent_node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected1 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(parent_node1.to_html(), expected1)

    def test_nested_node1_to_html(self):
        nested_node1 = ParentNode(
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
        expected = "<div><div><ul><li>Hyper Focus</li><li>Deep Work</li><li>Ultra Learning</li></ul></div><span>Colored text</span>Ordinary text<i>italic text</i>Normal text</div>"
        self.assertEqual(nested_node1.to_html(), expected)

    def test_nested_node2_to_html(self):
        nested_node2 = ParentNode(
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
        expected = "<div><p><b>Bold inside inner paragraph</b>Normal inside inner paragraph</p>Normal text inside outer div</div>"
        self.assertEqual(nested_node2.to_html(), expected)

    def test_edge_case(self):
        one_child_node = ParentNode(
            "ul", [ParentNode("li", [LeafNode(None, "Single list item")])]
        )
        expected = "<ul><li>Single list item</li></ul>"
        self.assertEqual(one_child_node.to_html(), expected)
