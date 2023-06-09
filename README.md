# impllmentors

impllmentors is a POC project demonstrating the emerging approach of structured and flow-controlled LLM agents
(as opposed to freely roaming agents as in AutoGPT and BabyAGI).

It is humble, and can only implement simple python modules. 
However simple, it also:
- Has well-defined structure and steps, avoids running in circles.
- Asks for human feedback between steps.
- Writes unit tests.
- Runs the unit tests, and if they fail, tries to fix the code/

## How To Use
1. Clone the repository: `git clone https://github.com/stavshamir/impllmentors.git`
2. Run `pip install -f requirements.txt`
3. Set an `OPENAI_API_KEY` environment variable
4. Run `python runner.py`

## Other Things To Consider
- The generated code and tests are written to the directory from which you run the script.
- You can view the written files and edit them between steps to help the AI.
- After the unit tests are written, the AI will not attempt to fix them in case they fail.
- This uses gpt-3.5-turbo, as I (and many others) still don't have access to the gpt-4 api. This means that hallucinations still happen quite often.

## Demo
(Sorry for the low quality)
![demo](https://github.com/stavshamir/impllmentors/blob/master/impllmentors.gif)



## Contribution
Feel free to suggest improvements and provide PRs!
