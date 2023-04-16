import unittest
from markdown_parser import parse_code_blocks, CodeBlock


class TestParseCodeBlocks(unittest.TestCase):

    def test_no_code_blocks(self):
        # Given
        markdown_text = "This is regular markdown text."

        # When
        code_blocks = parse_code_blocks(markdown_text)

        # Then
        self.assertEqual(len(code_blocks), 0)

    def test_single_code_block(self):
        # Given
        markdown_text = "Here is a code block: \n```python\nprint('hello world')\n```"

        # When
        code_blocks = parse_code_blocks(markdown_text)

        # Then
        self.assertEqual(len(code_blocks), 1)
        self.assertEqual(code_blocks[0].language, "python")
        self.assertEqual(code_blocks[0].code, "print('hello world')")

    def test_multiple_code_blocks(self):
        # Given
        markdown_text = "This is a markdown text. \n" \
                        "```python\nprint('hello world')\n```\n" \
                        " This is another markdown text. ```javascript\nconsole.log('hello world')\n```"

        # When
        code_blocks = parse_code_blocks(markdown_text)

        # Then
        self.assertEqual(len(code_blocks), 2)
        self.assertEqual(code_blocks[0].language, "python")
        self.assertEqual(code_blocks[0].code, "print('hello world')")
        self.assertEqual(code_blocks[1].language, "javascript")
        self.assertEqual(code_blocks[1].code, "console.log('hello world')")

    def test_no_language_specified(self):
        # Given
        markdown_text = "Here is a code block without a language specified: \n```\nprint('hello world')\n```"

        # When
        code_blocks = parse_code_blocks(markdown_text)

        # Then
        self.assertEqual(len(code_blocks), 1)
        self.assertEqual(code_blocks[0].language, None)
        self.assertEqual(code_blocks[0].code, "print('hello world')")

    def test_no_triple_backticks(self):
        # Given
        markdown_text = "Here is a code block without triple backticks: \n`print('hello world')`"

        # When
        code_blocks = parse_code_blocks(markdown_text)

        # Then
        self.assertEqual(len(code_blocks), 0)