import unittest

from textnode import TextNode
from inline import split_nodes_delimiter


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
