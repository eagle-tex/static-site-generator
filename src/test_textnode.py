import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)
        self.assertEqual(node, node3)

    def test_eq_with_url(self):
        node1 = TextNode("This is a text node", "italic", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "italic", "https://www.boot.dev")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", "italic", "https://www.boot.dev")
        node2 = TextNode(
            "This is a another text node", "italic", "https://www.boot.dev"
        )
        node3 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node4 = TextNode(
            "This is a text node",
            "bold",
        )
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node3, node4)


if __name__ == "__main__":
    unittest.main()
