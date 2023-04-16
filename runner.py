from rich import print
from rich.prompt import Prompt

from analyzer import Analyzer
from common import BOT_PREFIX
from fixer import Fixer
from implementor import Implementor
from tester import Tester


def write_file(file_name: str, content: str) -> None:
    with open(file_name, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    requirements = Prompt.ask(f'{BOT_PREFIX} Hi! What would you like to build?\n[green_yellow]YOU[/green_yellow]')

    print(
        '\n[bold deep_sky_blue1]Analyzing Requirement[/bold deep_sky_blue1] -> [grey30]Implementing[/grey30] -> [grey30]Writing Unit Tests[/grey30] -> [grey30]Verifying Tests Are Passing[/grey30]\n')
    module = Analyzer(requirements).analyze()

    print(
        '\n[green3]Analyzing Requirement[/green3] -> [bold deep_sky_blue1]Implementing[/bold deep_sky_blue1] -> [grey30]Writing Unit Tests[/grey30] -> [grey30]Verifying Tests Are Passing[/grey30]\n')
    implementation = Implementor(module).implement()
    write_file(f'{module.name}.py', implementation)
    print(f'{BOT_PREFIX} I have written the file {module.name}.py')

    print(
        '\n[green3]Analyzing Requirement[/green3] -> [green3]Implementing[/green3] -> [bold deep_sky_blue1]Writing Unit Tests[/bold deep_sky_blue1] -> [grey30]Verifying Tests Are Passing[/grey30]\n')
    tests = Tester(f'{module.name}.py').write_tests()
    write_file(f'test_{module.name}.py', tests)
    print(f'{BOT_PREFIX} I have written the file test_{module.name}.py')

    Prompt.ask(
        '[light_goldenrod3]BOT:[/light_goldenrod3] Review the module and tests, then press Enter to run the tests and fix the module if necessary')
    print(
        '\n[green3]Analyzing Requirement[/green3] -> [green3]Implementing[/green3] -> [green3]Writing Unit Tests[/green3] -> [bold deep_sky_blue1]Verifying Tests Are Passing[/bold deep_sky_blue1]')
    Fixer(module.name).run_tests_and_fix_if_needed()
