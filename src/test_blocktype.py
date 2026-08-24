

import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        blocks = [
            "> This is a quote",
            "> This is a multiline quote\n> that spans multiple lines"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_multiline_quote(self):
        block = "> This is a quote\n> that spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        blocks = [
            "- Item 1",
            "- Item 1\n- Item 2\n- Item 3"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        blocks = [
            "1. Item 1",
            "1. Item 1\n2. Item 2\n3. Item 3"
        ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_invalid_ordered_list(self):
        block = "1. Item 1\n3. Item 2\n2. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)