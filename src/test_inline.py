import unittest

from textnode import TextNode
from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_img(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertEqual(len(extract_markdown_images(text)), 2)
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(len(extract_markdown_links(text)), 2)
        self.assertEqual(extract_markdown_links(text), expected)


class TestSplitNodeImage(unittest.TestCase):
    def test_split_node_img1(self):
        node1 = TextNode(
            "This is text with an ![first image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        expected1 = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "first image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(len(split_nodes_image([node1])), 4)
        self.assertEqual(split_nodes_image([node1]), expected1)

    def test_split_node_img2(self):
        node2 = TextNode(
            "![third image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3idvOCJ.png) and another ![fourth image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/4unPdYb.png)",
            "text",
        )
        expected2 = [
            TextNode(
                "third image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3idvOCJ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "fourth image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/4unPdYb.png",
            ),
        ]
        self.assertEqual(len(split_nodes_image([node2])), 3)
        self.assertEqual(split_nodes_image([node2]), expected2)

    def test_split_node_img3(self):
        node3 = TextNode(
            "![fifth image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/5llwMBT.png)",
            "text",
        )
        expected3 = [
            TextNode(
                "fifth image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/5llwMBT.png",
            ),
        ]
        self.assertEqual(len(split_nodes_image([node3])), 1)
        self.assertEqual(split_nodes_image([node3]), expected3)

    def test_split_node_img4(self):
        node4 = TextNode("Only text", "text")
        expected4 = [TextNode("Only text", "text")]
        self.assertEqual(len(split_nodes_image([node4])), 1)
        self.assertEqual(split_nodes_image([node4]), expected4)

    def test_split_node_img_italic(self):
        node5 = TextNode("Text with *italic words* inside", "text")
        expected5 = [TextNode("Text with *italic words* inside", "text")]
        self.assertEqual(len(split_nodes_image([node5])), 1)
        self.assertEqual(split_nodes_image([node5]), expected5)

    def test_split_node_img_many(self):
        node1 = TextNode(
            "This is text with an ![first image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        node2 = TextNode(
            "![third image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3idvOCJ.png) and another ![fourth image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/4unPdYb.png)",
            "text",
        )
        node3 = TextNode(
            "![fifth image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/5llwMBT.png)",
            "text",
        )
        node4 = TextNode("Only text", "text")
        node5 = TextNode("Text with *italic words* inside", "text")
        expected_many = split_nodes_image([node1, node2, node3, node4, node5])
        self.assertEqual(len(expected_many), 10)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_node_link1(self):
        node1 = TextNode(
            "This is text with a [first link](https://www.example.com) and [another](https://www.example.com/another)",
            "text",
        )
        expected1 = split_nodes_link([node1])
        self.assertEqual(len(expected1), 4)
        self.assertEqual(expected1[0], TextNode("This is text with a ", "text"))
        self.assertEqual(
            expected1[1], TextNode("first link", "link", "https://www.example.com")
        )
        self.assertEqual(expected1[2], TextNode(" and ", "text"))
        self.assertEqual(
            expected1[3], TextNode("another", "link", "https://www.example.com/another")
        )

    def test_split_node_link2(self):
        node2 = TextNode(
            "This is text with only [one link](https://www.example.com)",
            "text",
        )
        expected2 = split_nodes_link([node2])
        self.assertEqual(len(expected2), 2)
        self.assertEqual(expected2[0], TextNode("This is text with only ", "text"))
        self.assertEqual(
            expected2[1], TextNode("one link", "link", "https://www.example.com")
        )

    def test_split_node_link3(self):
        node3 = TextNode(
            "[only the link](https://www.example.com)",
            "text",
        )
        expected3 = split_nodes_link([node3])
        self.assertEqual(len(expected3), 1)
        self.assertEqual(
            expected3[0], TextNode("only the link", "link", "https://www.example.com")
        )

    def test_split_node_link4(self):
        node4 = TextNode(
            "This node has only text",
            "text",
        )
        expected4 = split_nodes_link([node4])
        self.assertEqual(len(expected4), 1)
        self.assertEqual(expected4[0], TextNode("This node has only text", "text"))

    def test_split_node_link_many(self):
        node1 = TextNode(
            "This is text with a [first link](https://www.example.com) and [another](https://www.example.com/another)",
            "text",
        )
        node2 = TextNode(
            "This is text with only [one link](https://www.example.com)",
            "text",
        )
        node3 = TextNode(
            "[only the link](https://www.example.com)",
            "text",
        )
        node4 = TextNode(
            "This node has only text",
            "text",
        )
        expected_many = split_nodes_link([node1, node2, node3, node4])
        self.assertEqual(len(expected_many), 8)
        self.assertEqual(expected_many[0], TextNode("This is text with a ", "text"))
        self.assertEqual(
            expected_many[1], TextNode("first link", "link", "https://www.example.com")
        )
        self.assertEqual(expected_many[2], TextNode(" and ", "text"))
        self.assertEqual(
            expected_many[3],
            TextNode("another", "link", "https://www.example.com/another"),
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_empty_string(self):
        result = text_to_textnodes("")
        self.assertEqual(result, [])

    def test_plain_text(self):
        result = text_to_textnodes("Just a plain text")
        expected = [TextNode("Just a plain text", "text")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        result = text_to_textnodes(
            "![image1](url1)![image2](url2)[link1](url3)[link2](url4)"
        )
        expected = [
            TextNode("image1", "image", "url1"),
            TextNode("image2", "image", "url2"),
            TextNode("link1", "link", "url3"),
            TextNode("link2", "link", "url4"),
        ]
        self.assertEqual(result, expected)

    def test_only_special_formatting(self):
        result = text_to_textnodes("**bold** and *italic*")
        expected = [
            TextNode("bold", "bold"),
            TextNode(" and ", "text"),
            TextNode("italic", "italic"),
        ]
        self.assertEqual(result, expected)

    def test_txt_to_text_nodes_many(self):
        text_type_bold = "bold"
        text_type_code = "code"
        text_type_image = "image"
        text_type_italic = "italic"
        text_type_link = "link"
        text_type_text = "text"

        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 10)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
