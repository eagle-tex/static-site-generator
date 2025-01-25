import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_hello(self):
        input = "# Hello"
        output = extract_title(input)
        self.assertEqual(output, "Hello")

    def test_extract_title_hello_and_trim(self):
        input = "  # Hello  "
        output = extract_title(input)
        self.assertEqual(output, "Hello")

    def test_extract_only_one_level1_heading(self):
        input = "## Hello\n# World"
        output = extract_title(input)
        self.assertEqual(output, "World")

    def test_extract_first_level1_heading(self):
        input = "# Hello\n# World"
        output = extract_title(input)
        self.assertEqual(output, "Hello")

    def test_extract_raises_exception_for_empty_input(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_extract_raises_exception_if_no_heading_found_in_input(self):
        input = "Hello\nWorld"
        with self.assertRaises(Exception):
            extract_title(input)
