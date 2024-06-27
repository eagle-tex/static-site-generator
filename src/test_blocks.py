import unittest

from blocks import block_to_block_type, markdown_to_html_node, markdown_to_text
from htmlnode import flatten_html_element


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
            "* This is a list item\n    * This is second list item",
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
            "1. element 1\n2. element 2\n element 3",  # wrong ordered list syntax: jump from 2 to 4
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


def concatenate_result(lines):
    str = ""
    for line in lines:
        str += line.strip()
    return str


class TestMarkdownToHtml(unittest.TestCase):
    def test_simple_paragraph(self):
        simple_paragraph = "This is a simple paragraph."
        result = markdown_to_html_node(simple_paragraph)
        flat_result = flatten_html_element(result.to_html())
        expected = "<div><p>This is a simple paragraph.</p></div>"
        self.assertEqual(flat_result, expected)

    def test_multiple_paragraphs(self):
        markdown = """This is the first paragraph.

This is the second paragraph."""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result.to_html())
        expected = "<div><p>This is the first paragraph.</p><p>This is the second paragraph.</p></div>"
        self.assertEqual(flat_result, expected)

    def test_headings(self):
        markdown = """# Heading 1
## Heading 2
### Heading 3"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result.to_html())
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        self.assertEqual(flat_result, expected)

    def test_unordered_list(self):
        markdown = """- Item 1
- Item 2
 - Item 2.1
 - Item 2.2"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result.to_html())
        expected = "<div><ul><li>Item 1</li><li>Item 2<ul><li>Item 2.1</li><li>Item 2.2</li></ul></li></ul></div>"
        self.assertEqual(flat_result, expected)

    def test_ordered_list(self):
        markdown = """1. First
2. Second
 3. Second.1
 4. Second.2"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result.to_html())
        expected = "<div><ol><li>First</li><li>Second<ol><li>Second.1</li><li>Second.2</li></ol></li></ol></div>"
        self.assertEqual(flat_result, expected)

    def test_mixed_list_one(self):
        markdown = """- Item 1
 1. Subitem 1
 2. Subitem 2
- Item 2"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result.to_html())
        expected = "<div><ul><li>Item 1<ol><li>Subitem 1</li><li>Subitem 2</li></ol></li><li>Item 2</li></ul></div>"
        self.assertEqual(flat_result, expected)

    def test_mixed_list_two(self):
        markdown = """1. item 1 ordered
2. item 2 ordered
  + item 2.1 unordered
  + item 2.2 unordered
    1. item 2.2.1 ordered
    2. item 2.2.2 ordered
  * item 2.3 unordered
  - item 2.4 unordered
    1. item 2.4.1 ordered
    2. item 2.4.2 ordered
      - item 2.4.2.1 unordered
      * item 2.4.2.2 unordered
3. item 3 ordered"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result.to_html())
        expected = "<div><ol><li>item 1 ordered</li><li>item 2 ordered<ul><li>item 2.1 unordered</li><li>item 2.2 unordered<ol><li>item 2.2.1 ordered</li><li>item 2.2.2 ordered</li></ol></li><li>item 2.3 unordered</li><li>item 2.4 unordered<ol><li>item 2.4.1 ordered</li><li>item 2.4.2 ordered<ul><li>item 2.4.2.1 unordered</li><li>item 2.4.2.2 unordered</li></ul></li></ol></li></ul></li><li>item 3 ordered</li></ol></div>"
        self.assertEqual(flat_result, expected)

    def test_blockquote(self):
        markdown = """> This is a quote"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result.to_html())
        expected = "<div><blockquote><p>This is a quote</p></blockquote></div>"
        self.assertEqual(flat_result, expected)

    def test_code_block(self):
        markdown = """```python3
def hello_world():
    print("Hello, world!")```"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result.to_html())
        expected = '<div><pre><code>def hello_world():print("Hello, world!")</code></pre></div>'
        self.assertEqual(flat_result, expected)

    def test_combined_elements(self):
        markdown = """# Heading 1

This is a paragraph.

- Item 1
- Item 2

> This is a quote

1. First item
2. Second item"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result)
        expected = "<div><h1>Heading 1</h1><p>This is a paragraph.</p><ul><li>Item 1</li><li>Item 2</li></ul><blockquote><p>This is a quote</p></blockquote><ol><li>First item</li><li>Second item</li></ol></div>"
        self.assertEqual(flat_result, expected)

    def test_nested_code_block_in_list(self):
        markdown = """- Item 1
 - Subitem with code:
    ```
    def nested_code():
        pass
    ```
- Item 2"""
        result = markdown_to_html_node(markdown)
        flat_result = flatten_html_element(result)
        expected = ""
        self.assertEqual(flat_result, expected)
