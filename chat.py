import os
from dataclasses import dataclass

import openai as openai
import rich
from halo import Halo
from rich.prompt import Prompt

from common import BOT_PREFIX

api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print('OPENAI_API_KEY is not set!')
    exit(1)

openai.api_key = api_key


@dataclass
class ChatMessage:
    role: str
    content: str

    @classmethod
    def of_system(cls, content):
        return cls('system', content)

    @classmethod
    def of_assistant(cls, content):
        return cls('assistant', content)

    @classmethod
    def of_user(cls, content):
        return cls('user', content)

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }


class ChatHistory:
    def __init__(self, messages: list[ChatMessage]):
        self.messages = messages

    def append_message(self, message: ChatMessage):
        self.messages.append(message)

    def to_array_of_dicts(self) -> list[dict[str, str]]:
        return [
            message.to_dict() for message in self.messages
        ]

    def last_assistant_reply(self):
        if len(self.messages) != 0 and self.messages[-1].role == 'assistant':
            return self.messages[-1].content
        else:
            return None


class Chat:
    def __init__(self, messages: list[ChatMessage], model='gpt-3.5-turbo'):
        self.model = model
        self.chat_history = ChatHistory(messages)

    def run(self) -> ChatHistory:
        with Halo(text='Thinking...', spinner='dots'):
            result = openai.ChatCompletion.create(model=self.model, messages=self.chat_history.to_array_of_dicts())

        content = result['choices'][0]['message']['content']
        self.chat_history.append_message(ChatMessage.of_assistant(content))
        return self.chat_history


class ChatWithHumanFeedback:
    def __init__(self, messages: list[ChatMessage], model='gpt-3.5-turbo'):
        self.model = model
        self.chat_history = ChatHistory(messages)

    def run(self) -> ChatHistory:
        while True:
            with Halo(text='Thinking...', spinner='dots'):
                result = openai.ChatCompletion.create(model=self.model, messages=self.chat_history.to_array_of_dicts())

            content = result['choices'][0]['message']['content']
            self.chat_history.append_message(ChatMessage.of_assistant(content))
            print(content)

            user_input = input("Do you have any comments? If not just press Enter.")

            if not user_input:
                return self.chat_history

            self.chat_history.append_message(ChatMessage.of_assistant(content))
            self.chat_history.append_message(ChatMessage.of_user(user_input))


class ChatWithCallback:
    def __init__(self, callback, messages: list[ChatMessage], model='gpt-3.5-turbo'):
        self.model = model
        self.chat_history = ChatHistory(messages)
        self.callback = callback

    def run(self):
        while True:
            with Halo(text='Thinking...', spinner='dots'):
                response = openai.ChatCompletion.create(model=self.model,
                                                        messages=self.chat_history.to_array_of_dicts())

            content = response['choices'][0]['message']['content']
            self.chat_history.append_message(ChatMessage.of_assistant(content))
            result = self.callback(content)

            user_input = Prompt.ask(f"{BOT_PREFIX} Do you have any comments? If not just press Enter")

            if not user_input:
                rich.print(f'{BOT_PREFIX} OK, I will continue')
                return result

            rich.print(f'{BOT_PREFIX} OK, I will try again')
            self.chat_history.append_message(ChatMessage.of_assistant(content))
            self.chat_history.append_message(ChatMessage.of_user(user_input))
