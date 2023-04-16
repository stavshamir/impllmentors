import rich
import yaml
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.data import YamlLexer

import markdown_parser
from chat import ChatMessage, ChatWithCallback
from common import ModuleDetails


def parse_and_print(content: str) -> str:
    blocks = markdown_parser.parse_code_blocks(content)
    code = blocks[0].code
    rich.print('[light_goldenrod3]BOT:[/light_goldenrod3] Here is an overview of the module you required.')
    print(highlight(code, YamlLexer(), TerminalFormatter()))
    return code


class Analyzer:
    def __init__(self, requirements: str):
        self.requirements = requirements
        self.analyze_and_review_chat: ChatWithCallback = self._create_analyze_and_review_chat()

    def _create_analyze_and_review_chat(self):
        prompt = f'''
        Your are a very experienced python software developer. 
        Write the api for a module based on its description.

        The API should contain the module's name and public functions signatures and doc strings.

        For example, given the following text:
        Given a markdown file containing code blocks, I want to extract the code blocks.

        The answer may be:
        ```yaml
        name: markdown_utils
        description: A module for markdown-related utility functions
        api: |
          def extract_code_blocks(text: str) -> list[str]:
              """
              Extracts code blocks from a markdown text.

              Args:
              text: A string that may or may not contain markdown code blocks.

              Returns:
              All the code blocks identified in the given text. If no code blocks were found, return an empty list.
              """
        ```

        Reply only with a valid yaml, formatted as in the example.

        Description: {self.requirements}
        Response:
        <formatted yaml>
        '''

        return ChatWithCallback(callback=parse_and_print, messages=[
            ChatMessage.of_system('You are an experienced python software engineer.'),
            ChatMessage.of_user(prompt)
        ])

    @staticmethod
    def _parse_response(response: str) -> ModuleDetails:
        yaml_data = yaml.safe_load(response)

        return ModuleDetails(
            name=yaml_data['name'],
            description=yaml_data['description'],
            api=yaml_data['api']
        )

    def analyze(self) -> ModuleDetails:
        reviewed_analysis = self.analyze_and_review_chat.run()
        return self._parse_response(reviewed_analysis)
