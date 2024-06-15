import unittest

from blocks import block_to_block_type, markdown_to_text


class TestMarkdownToText(unittest.TestCase):
    def test_empty_string(self):
        result = markdown_to_text("")
        self.assertEqual(result, [])

    def test_string_with_only_spaces(self):
        result = markdown_to_text("     ")
        self.assertEqual(result, [])

    def test_simple_markdown(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            f"* This is a list item\n* This is another list item",
        ]
        result = markdown_to_text(markdown)
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_markdown_with_multiple_blank_lines(self):
        markdown = """
# This is a heading       
## This is a sub-heading


         This is a paragraph of text.  
    It has some **bold** and *italic* words inside of it.   
      

* This is a list item
    * This is second list item    
        
        """
        result = markdown_to_text(markdown)
        expected = [
            "# This is a heading\n## This is a sub-heading",
            "This is a paragraph of text.\nIt has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is second list item",
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)


class TestBlockToBlock(unittest.TestCase):
    def test_block_type_one_of_each(self):
        blocks = [
            "# Heading\n## Sub-heading",
            ">a quote block\n>second quote\n>third quote",
            "* element 1\n* element 2\n* element 3",
            "```py\nprint('hello')\n```",
            "1. element 1\n2. element 2\n3. element 3",
            "this is a paragraph\nof text",
        ]
        expected = []
        for block in blocks:
            expected.append(block_to_block_type(block))

        self.assertEqual(
            expected,
            ["heading", "quote", "unordered_list", "code", "ordered_list", "paragraph"],
        )

    def test_block_type_all_paragraphs(self):
        blocks = [
            "#Heading\n## Sub-heading",  # wrong syntax on '#Heading'
            ">a quote block\n >second quote\n>third quote",  # wrong quote syntax on 'second quote'
            "*element 1\n* element 2\n* element 3",  # wrong unordered list syntax on 1 element
            "```py\nprint('hello')\n``",  # code block not closed properly: 2 back ticks instead of 3
            "1. element 1\n2. element 2\n4. element 3",  # wrong ordered list syntax: jump from 2 to 4
        ]
        expected = []
        for block in blocks:
            expected.append(block_to_block_type(block))

        self.assertEqual(
            expected,
            ["paragraph", "paragraph", "paragraph", "paragraph", "paragraph"],
        )

    def test_block_empty_string_raises(self):
        block = ""
        with self.assertRaises(ValueError):
            block_to_block_type(block)
