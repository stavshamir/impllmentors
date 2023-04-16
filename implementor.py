import subprocess

import rich
import rich.prompt
import yaml
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.python import PythonLexer

import markdown_parser
from chat import ChatMessage, ChatWithCallback
from common import ModuleDetails, BOT_PREFIX


def parse_and_print(content: str) -> str:
    blocks = markdown_parser.parse_code_blocks(content)
    block = blocks[0].code if len(blocks) > 0 else content
    yaml_data = yaml.safe_load(block)
    code = yaml_data['code']

    rich.print(f'{BOT_PREFIX} Here is the implementation for the api we defined.')
    print(highlight(code, PythonLexer(), TerminalFormatter()))

    dependencies = yaml_data['dependencies']
    if dependencies and len(dependencies) > 0:
        rich.print(f'\n{BOT_PREFIX} You will need to install the following packages:')
        for dep in dependencies:
            rich.print(f'- {dep}')

        confirm = rich.prompt.Confirm.ask(f'{BOT_PREFIX} Do you want me to install them for you?')

        if confirm:
            for dep in dependencies:
                rich.print(f'{BOT_PREFIX} Installing {dep}')
                subprocess.run(['pip', 'install', dep])

    return code


class Implementor:
    def __init__(self, module: ModuleDetails):
        self.module: ModuleDetails = module
        self.implement_and_review_chat: ChatWithCallback = self._create_implement_and_review_chat()

    def _create_implement_and_review_chat(self):
        prompt = f'''
        You will be given module details and API. Provide an implementation of the module given the following instructions:

        - You must not change the function signatures and the doc strings described in the api.
        - If non-standard library packages are required, specify them in the `dependencies`.
        - If only standard library packages are needed, no need to specify anything in the `dependencies`.
        - Reply only with a valid yaml.

        Module name: {self.module.name}
        Module description: {self.module.description}
        Module api: {self.module.api}
        
        Response:
        ```yaml
        dependencies:
            - <package 1 to install>
            - <package 2 to install>
            ...
        code: |
            <The requested module code, including the docstring>
        ```
        '''

        return ChatWithCallback(callback=parse_and_print, messages=[
            ChatMessage.of_system('You are an experienced python software engineer.'),
            ChatMessage.of_user(prompt)
        ])

    def implement(self) -> str:
        return self.implement_and_review_chat.run()
