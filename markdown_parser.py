import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CodeBlock:
    """
    Represents a code block identified in a markdown text.

    Attributes:
        language: An optional string representing the language of the code block.
        code: A string representing the code contained in the code block.
    """
    language: Optional[str]
    code: str


def parse_code_blocks(markdown_text: str) -> List[CodeBlock]:
    """
    Parses a markdown text and extracts all the code blocks found in it.

    Args:
        markdown_text: a string containing markdown that may or may not contain code blocks.

    Returns:
        A list of CodeBlock objects representing all the identified code blocks in the markdown text. If no code blocks
        were found, return an empty list.
    """
    code_blocks = []
    pattern = re.compile(r"```(\w+)?\n(.+?)\n```", flags=re.DOTALL | re.MULTILINE)
    for match in pattern.finditer(markdown_text):
        language, code = match.groups()
        code_blocks.append(CodeBlock(language, code))
    return code_blocks
