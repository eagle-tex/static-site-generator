import unittest

from leafnode import LeafNode
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

    def test_text_node_to_html(self):
        text_node = TextNode("This is a TEXT text node", "text")
        self.assertEqual(isinstance(text_node.text_node_to_html_node(), LeafNode), True)
        self.assertEqual(text_node.text_node_to_html_node().to_html(), text_node.text)

    def test_bold_node_to_html(self):
        bold_text_node = TextNode("This is a BOLD text node", "bold")
        self.assertEqual(
            isinstance(bold_text_node.text_node_to_html_node(), LeafNode), True
        )
        self.assertEqual(
            bold_text_node.text_node_to_html_node().to_html(),
            LeafNode("b", bold_text_node.text).to_html(),
        )

    def test_italic_node_to_html(self):
        italic_text_node = TextNode("This is a ITALIC text node", "italic")
        self.assertEqual(
            isinstance(italic_text_node.text_node_to_html_node(), LeafNode), True
        )
        self.assertEqual(
            italic_text_node.text_node_to_html_node().to_html(),
            LeafNode("i", italic_text_node.text).to_html(),
        )

    def test_code_node_to_html(self):
        code_text_node = TextNode("This is a CODE text node", "code")
        self.assertEqual(
            isinstance(code_text_node.text_node_to_html_node(), LeafNode), True
        )
        self.assertEqual(
            code_text_node.text_node_to_html_node().to_html(),
            LeafNode("code", code_text_node.text).to_html(),
        )

    def test_link_node_to_html(self):
        link_text_node = TextNode(
            "This is a LINK text node", "link", "https://www.boot.dev"
        )
        self.assertEqual(
            isinstance(link_text_node.text_node_to_html_node(), LeafNode), True
        )
        self.assertEqual(
            link_text_node.text_node_to_html_node().to_html(),
            LeafNode("a", link_text_node.text, {"href": link_text_node.url}).to_html(),
        )

    def test_image_node_to_html(self):
        img_text_node = TextNode(
            "This is a IMAGE text node", "image", "/assets/background1.jpg"
        )
        self.assertEqual(
            isinstance(img_text_node.text_node_to_html_node(), LeafNode), True
        )
        self.assertEqual(
            img_text_node.text_node_to_html_node().to_html(),
            LeafNode(
                "img",
                "",
                {"src": img_text_node.url, "alt": img_text_node.text},
            ).to_html(),
        )

    def test_pdf_node_to_html(self):
        pdf_text_node = TextNode("This is a PDF text node", "pdf")
        with self.assertRaises(Exception):
            pdf_text_node.text_node_to_html_node()


if __name__ == "__main__":
    unittest.main()
