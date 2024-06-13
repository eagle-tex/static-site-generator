import unittest

from leafnode import LeafNode
from textnode import TextNode, split_nodes_delimiter


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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_code(self):
        text_type_code = "code"
        text_type_text = "text"

        node1 = TextNode("This is a text with a `code block` word", text_type_text)
        new_nodes1 = split_nodes_delimiter([node1], "`", text_type_code)
        self.assertEqual(len(new_nodes1), 3)
        self.assertEqual(
            new_nodes1[0], TextNode("This is a text with a ", text_type_text)
        )
        self.assertEqual(new_nodes1[1], TextNode("code block", text_type_code))
        self.assertEqual(new_nodes1[2], TextNode(" word", text_type_text))

    def test_split_nodes_italic(self):
        text_type_italic = "italic"
        text_type_text = "text"

        node2 = TextNode("A second text with an *italic* word", text_type_text)
        new_nodes2 = split_nodes_delimiter([node2], "*", text_type_italic)
        self.assertEqual(len(new_nodes2), 3)
        self.assertEqual(
            new_nodes2[0], TextNode("A second text with an ", text_type_text)
        )
        self.assertEqual(new_nodes2[1], TextNode("italic", text_type_italic))
        self.assertEqual(new_nodes2[2], TextNode(" word", text_type_text))

    def test_split_nodes_bold(self):
        text_type_bold = "bold"
        text_type_text = "text"

        node3 = TextNode("A third one with a **bold** word", text_type_text)
        new_nodes3 = split_nodes_delimiter([node3], "**", text_type_bold)
        self.assertEqual(len(new_nodes3), 3)
        self.assertEqual(new_nodes3[0], TextNode("A third one with a ", text_type_text))
        self.assertEqual(new_nodes3[1], TextNode("bold", text_type_bold))
        self.assertEqual(new_nodes3[2], TextNode(" word", text_type_text))

    def test_split_nodes_text(self):
        text_type_bold = "bold"
        text_type_text = "text"

        node4 = TextNode("This is a normal text with no delimiter", text_type_text)
        new_nodes4 = split_nodes_delimiter([node4], "**", text_type_bold)
        self.assertEqual(len(new_nodes4), 1)
        self.assertEqual(
            new_nodes4[0],
            TextNode("This is a normal text with no delimiter", text_type_text),
        )

    def test_split_nodes_link(self):
        text_type_italic = "italic"

        node5 = TextNode("This is a text with a link", "link", {"url": "www.maped.com"})
        new_nodes5 = split_nodes_delimiter([node5], "*", text_type_italic)
        self.assertEqual(len(new_nodes5), 1)
        self.assertEqual(new_nodes5[0], node5)

    def test_split_demiliter_raises(self):
        node6 = TextNode("A text with only one `backtick is not parsable", "text")
        with self.assertRaises(Exception):
            split_nodes_delimiter([node6], "`", "code")


if __name__ == "__main__":
    unittest.main()
