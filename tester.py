import rich
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.python import PythonLexer

import markdown_parser
from chat import ChatMessage, ChatWithCallback
from common import BOT_PREFIX


def parse_and_print(content: str) -> str:
    blocks = markdown_parser.parse_code_blocks(content)
    code = blocks[0].code
    rich.print(f'{BOT_PREFIX} I wrote some unit tests to verify the modules behavior.')
    print(highlight(code, PythonLexer(), TerminalFormatter()))
    return code


class Tester:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.file_content: str = self._load_content()
        self.write_tests_and_review_chat: ChatWithCallback = self._create_write_tests_and_review_chat()

    def _load_content(self) -> str:
        with open(self.file_name, 'r') as f:
            return f.read()

    def _create_write_tests_and_review_chat(self):
        prompt = f'''
        Write a unit tests file for the module {self.file_name}.
        Each unit test method should ideally contain only few assertions.
        Each case should be in its own test method.
        Don't forget to consider edge cases and inputs.
        
        Each test method must have the following structure, including the comments:
        ```python
        def test_<case_description>(self):
            # Given <short description of setting up the input to the function under test>
            <Setting up the input to the function under test>    
            
            # When
            <call function under test and get its return value>
            
            # Then <short description of expected outcome>
            <assertions>
        ```
        
        This is the content of the module:
        ```python
        {self.file_content}
        ```
        
        Provide code only without explanations:
        ```python
        <unit tests>
        ```
        '''

        return ChatWithCallback(callback=parse_and_print, messages=[
            ChatMessage.of_system('You are an experienced python software engineer.'),
            ChatMessage.of_user(prompt)
        ])

    def _create_suggest_cases_chat(self):
        prompt = f'''
        Suggest a list of unit tests for the module {self.file_name}.
        Each item in the list should be a short description (one or two sentences at most) of the unit tests.
        Don't forget to consider edge cases and inputs.

        This is the content of the module:
        ```python
        {self.file_content}
        ```

        Suggestions:
        1. <First suggestion>
        2. <Second suggestions>
        ...
        '''

        return ChatWithCallback(callback=print, messages=[
            ChatMessage.of_system('You are an experienced python software engineer.'),
            ChatMessage.of_user(prompt)
        ])

    def write_tests(self) -> str:
        return self.write_tests_and_review_chat.run()
