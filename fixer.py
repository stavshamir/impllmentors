import subprocess

import rich
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.python import PythonLexer
from rich.prompt import Prompt

import markdown_parser
from chat import ChatMessage, Chat
from common import BOT_PREFIX


class Fixer:
    def __init__(self, module_name: str, max_tries: int = 3):
        self.module_name = module_name
        self.module_content: str = self._load_content(f'{module_name}.py')
        self.test_module_file_name = f'test_{module_name}.py'
        self.module_tests_content: str = self._load_content(self.test_module_file_name)
        self.max_tries = max_tries

    @staticmethod
    def _load_content(file_name: str) -> str:
        with open(file_name, 'r') as f:
            return f.read()

    def _create_chat(self, stderr: str):
        prompt = f'''
        Below, you are given the contents of a python module and the contents of the unit tests for that module.

        The contents of module {self.module_name}.py:
        ```python
        {self.module_content}
        ```

        The contents of the unit tests file {self.test_module_file_name}:
        ```python
        {self.module_tests_content}
        ```

        The unit tests are failing with the following message: {stderr}

        Fix the module so that the unit tests will pass. 
        The unit tests are the ultimate source of truth, do not try to change them!

        Provide code only without explanations:
        ```python
        <fixed code>
        ```
        '''

        return Chat(messages=[
            ChatMessage.of_system('You are an experienced python software engineer.'),
            ChatMessage.of_user(prompt)
        ])

    def run_tests_and_fix_if_needed(self):
        output = self.run_unit_tests()
        if output.returncode == 0:
            rich.print(f'{BOT_PREFIX} All unit tests are passing.')
            return

        stderr_summary = self.summarize_stderr(output.stderr)
        rich.print(f'{BOT_PREFIX} There are failing unit tests.')
        rich.print(f'{BOT_PREFIX} Here is a summary of the failures:')
        rich.print(f'{stderr_summary}')
        Prompt.ask(
            f'{BOT_PREFIX} I will try to fix the module. Please review the unit tests and press Enter when I can start')

        self.try_to_fix(output.stderr)

    def run_unit_tests(self):
        return subprocess.run(
            ['python', '-m', 'unittest', self.test_module_file_name],
            capture_output=True,
            text=True
        )

    def try_to_fix(self, stderr: str):
        chat = self._create_chat(stderr)
        for i in range(1, self.max_tries):
            chat_history = chat.run()
            response = chat_history.last_assistant_reply()
            fixed_module = markdown_parser.parse_code_blocks(response)[0].code

            rich.print(f'{BOT_PREFIX} I changed the code to this:')
            print(highlight(fixed_module, PythonLexer(), TerminalFormatter()))

            with open(f'{self.module_name}.py', 'w') as f:
                f.write(fixed_module)

            Prompt.ask(f'{BOT_PREFIX} Press Enter when you are ready from me to run the tests again')
            output = self.run_unit_tests()
            if output.returncode == 0:
                rich.print(f'{BOT_PREFIX} I fixed the module. All unit tests are now passing.')
                return

            chat_history.append_message(ChatMessage.of_user(
                f'The tests still fail after the changes you made. This is the stderr:\n {output.stderr}'))

            rich.print(f'''{BOT_PREFIX} Fix attempt {i}/{self.max_tries} has failed.
Here is a summary of the reasons: 
{self.summarize_stderr(output.stderr)}''')
        rich.print(
            f"{BOT_PREFIX} Fix attempt {self.max_tries}/{self.max_tries} has failed.")
        rich.print(f"{BOT_PREFIX} Sorry, I can't fix the module. Make sure the tests are correct.")

    def summarize_stderr(self, stderr: str) -> str:
        prompt = f'''
        Below, you are given the contents of a python module and the contents of the unit tests for that module.

        The contents of module {self.module_name}.py:
        ```python
        {self.module_content}
        ```

        The contents of the unit tests file {self.test_module_file_name}:
        ```python
        {self.module_tests_content}
        ```

        The unit tests are failing with the following message: {stderr}

        Explain and summarize the errors failing the test in context of the module and its tests.
        Do not explain the module code or recommend any fixes, just summarize the reasons for failure.
        
        Respond in the following format:
        1. Summary for error 1
        2. Summary for error 2
        ...
        '''

        return Chat(messages=[
            ChatMessage.of_system('You are an experienced python software engineer.'),
            ChatMessage.of_user(prompt)
        ]).run().last_assistant_reply()


if __name__ == '__main__':
    Fixer('config_utils').run_tests_and_fix_if_needed()
