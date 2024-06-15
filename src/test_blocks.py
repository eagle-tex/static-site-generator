import unittest

from blocks import markdown_to_text


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
