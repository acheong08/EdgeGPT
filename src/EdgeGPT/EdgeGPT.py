"""
Main.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Generator

from .chathub import *
from .conversation import *
from .conversation_style import *
from .request import *
from .utilities import *


class Chatbot:
    """
    Combines everything to make it seamless
    """

    def __init__(
        self,
        proxy: str | None = None,
        cookies: list[dict] | None = None,
    ) -> None:
        self.proxy: str | None = proxy
        self.chat_hub: ChatHub = ChatHub(
            Conversation(self.proxy, cookies=cookies),
            proxy=self.proxy,
            cookies=cookies,
        )

    @staticmethod
    async def create(
        proxy: str | None = None,
        cookies: list[dict] | None = None,
    ) -> Chatbot:
        self = Chatbot.__new__(Chatbot)
        self.proxy = proxy
        self.chat_hub = ChatHub(
            await Conversation.create(self.proxy, cookies=cookies),
            proxy=self.proxy,
            cookies=cookies,
        )
        return self

    async def save_conversation(self, filename: str) -> None:
        """
        Save the conversation to a file
        """
        with open(filename, "w") as f:
            conversation_id = self.chat_hub.request.conversation_id
            conversation_signature = self.chat_hub.request.conversation_signature
            client_id = self.chat_hub.request.client_id
            invocation_id = self.chat_hub.request.invocation_id
            f.write(
                {
                    "conversation_id": conversation_id,
                    "conversation_signature": conversation_signature,
                    "client_id": client_id,
                    "invocation_id": invocation_id,
                },
            )

    async def load_conversation(self, filename: str) -> None:
        """
        Load the conversation from a file
        """
        with open(filename) as f:
            conversation = json.load(f)
            self.chat_hub.request = ChatHubRequest(
                conversation_signature=conversation["conversation_signature"],
                client_id=conversation["client_id"],
                conversation_id=conversation["conversation_id"],
                invocation_id=conversation["invocation_id"],
            )

    async def get_conversation(self) -> dict:
        """
        Gets the conversation history from conversation_id (requires load_conversation)
        """
        return await self.chat_hub.get_conversation()

    async def ask(
        self,
        prompt: str,
        wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
        conversation_style: CONVERSATION_STYLE_TYPE = None,
        webpage_context: str | None = None,
        search_result: bool = False,
        locale: str = guess_locale(),
    ) -> dict:
        """
        Ask a question to the bot
        Response:
            {
                item (dict):
                    messages (list[dict]):
                        adaptiveCards (list[dict]):
                            body (list[dict]):
                                text (str): Response
            }
        To get the response, you can do:
            response["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
        """
        async for final, response in self.chat_hub.ask_stream(
            prompt=prompt,
            conversation_style=conversation_style,
            wss_link=wss_link,
            webpage_context=webpage_context,
            search_result=search_result,
            locale=locale,
        ):
            if final:
                if not self.chat_hub.wss.closed:
                    await self.chat_hub.wss.close()
                if not self.chat_hub.wss_session.closed:
                    await self.chat_hub.wss_session.close()
                return response
        return {}

    async def ask_stream(
        self,
        prompt: str,
        wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
        conversation_style: CONVERSATION_STYLE_TYPE = None,
        raw: bool = False,
        webpage_context: str | None = None,
        search_result: bool = False,
        locale: str = guess_locale(),
    ) -> Generator[bool, dict | str, None]:
        """
        Ask a question to the bot
        """
        async for response in self.chat_hub.ask_stream(
            prompt=prompt,
            conversation_style=conversation_style,
            wss_link=wss_link,
            raw=raw,
            webpage_context=webpage_context,
            search_result=search_result,
            locale=locale,
        ):
            yield response

    async def close(self) -> None:
        """
        Close the connection
        """
        await self.chat_hub.close()

    async def reset(self) -> None:
        """
        Reset the conversation
        """
        await self.close()
        self.chat_hub = ChatHub(
            await Conversation.create(self.proxy, cookies=self.chat_hub.cookies),
            proxy=self.proxy,
            cookies=self.chat_hub.cookies,
        )


import argparse, asyncio, json
from rich.live import Live
from rich.markdown import Markdown
from pathlib import Path
import re
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from EdgeGPT.EdgeGPT import Chatbot


def create_session() -> PromptSession:
    kb = KeyBindings()

    @kb.add("enter")
    def _(event) -> None:
        buffer_text = event.current_buffer.text
        if buffer_text.startswith("!"):
            event.current_buffer.validate_and_handle()
        else:
            event.current_buffer.insert_text("\n")

    @kb.add("escape")
    def _(event) -> None:
        if event.current_buffer.complete_state:
            # event.current_buffer.cancel_completion()
            event.current_buffer.text = ""

    return PromptSession(key_bindings=kb, history=InMemoryHistory())


def create_completer(commands: list, pattern_str: str = "$") -> WordCompleter:
    return WordCompleter(words=commands, pattern=re.compile(pattern_str))


def _create_history_logger(f):
    def logger(*args, **kwargs) -> None:
        tmp = sys.stdout
        sys.stdout = f
        print(*args, **kwargs, flush=True)
        sys.stdout = tmp

    return logger


async def get_input_async(
    session: PromptSession = None,
    completer: WordCompleter = None,
) -> str:
    """
    Multiline input function.
    """
    return await session.prompt_async(
        completer=completer,
        multiline=True,
        auto_suggest=AutoSuggestFromHistory(),
    )


async def async_main(args: argparse.Namespace) -> None:
    """
    Main function
    """
    print("Initializing...")
    print("Enter `alt+enter` or `escape+enter` to send a message")
    # Read and parse cookies
    cookies = None
    if args.cookie_file:
        file_path = Path(args.cookie_file)
        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as f:
                cookies = json.load(f)
    bot = await Chatbot.create(proxy=args.proxy, cookies=cookies)
    session = create_session()
    completer = create_completer(["!help", "!exit", "!reset"])
    initial_prompt = args.prompt

    # Log chat history
    def p_hist(*args, **kwargs) -> None:
        pass

    if args.history_file:
        history_file_path = Path(args.history_file)
        f = history_file_path.open("a+", encoding="utf-8")
        p_hist = _create_history_logger(f)

    while True:
        print("\nYou:")
        p_hist("\nYou:")
        if initial_prompt:
            question = initial_prompt
            print(question)
            initial_prompt = None
        else:
            question = (
                input()
                if args.enter_once
                else await get_input_async(session=session, completer=completer)
            )
        print()
        p_hist(question + "\n")
        if question == "!exit":
            break
        if question == "!help":
            print(
                """
            !help - Show this help message
            !exit - Exit the program
            !reset - Reset the conversation
            """,
            )
            continue
        if question == "!reset":
            await bot.reset()
            continue
        print("Bot:")
        p_hist("Bot:")
        if args.no_stream:
            response = (
                await bot.ask(
                    prompt=question,
                    conversation_style=args.style,
                    wss_link=args.wss_link,
                    search_result=args.search_result,
                    locale=args.locale,
                )
            )["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
            print(response)
            p_hist(response)
        else:
            wrote = 0
            if args.rich:
                md = Markdown("")
                with Live(md, auto_refresh=False) as live:
                    async for final, response in bot.ask_stream(
                        prompt=question,
                        conversation_style=args.style,
                        wss_link=args.wss_link,
                        search_result=args.search_result,
                        locale=args.locale,
                    ):
                        if not final:
                            if not wrote:
                                p_hist(response, end="")
                            else:
                                p_hist(response[wrote:], end="")
                            if wrote > len(response):
                                print(md)
                                print(Markdown("***Bing revoked the response.***"))
                            wrote = len(response)
                            md = Markdown(response)
                            live.update(md, refresh=True)
            else:
                async for final, response in bot.ask_stream(
                    prompt=question,
                    conversation_style=args.style,
                    wss_link=args.wss_link,
                    search_result=args.search_result,
                    locale=args.locale,
                ):
                    if not final:
                        if not wrote:
                            print(response, end="", flush=True)
                            p_hist(response, end="")
                        else:
                            print(response[wrote:], end="", flush=True)
                            p_hist(response[wrote:], end="")
                        wrote = len(response)
                print()
                p_hist()
    if args.history_file:
        f.close()
    await bot.close()


def main() -> None:
    print(
        """
        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit
    """,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--enter-once", action="store_true")
    parser.add_argument("--search-result", action="store_true")
    parser.add_argument("--no-stream", action="store_true")
    parser.add_argument("--rich", action="store_true")
    parser.add_argument(
        "--proxy",
        help="Proxy URL (e.g. socks5://127.0.0.1:1080)",
        type=str,
    )
    parser.add_argument(
        "--wss-link",
        help="WSS URL(e.g. wss://sydney.bing.com/sydney/ChatHub)",
        type=str,
        default="wss://sydney.bing.com/sydney/ChatHub",
    )
    parser.add_argument(
        "--style",
        choices=["creative", "balanced", "precise"],
        default="balanced",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="",
        required=False,
        help="prompt to start with",
    )
    parser.add_argument(
        "--cookie-file",
        type=str,
        default="",
        required=False,
        help="path to cookie file",
    )
    parser.add_argument(
        "--history-file",
        type=str,
        default="",
        required=False,
        help="path to history file",
    )
    parser.add_argument(
        "--locale",
        type=str,
        default="en-US",
        required=False,
        help="your locale",
    )
    args = parser.parse_args()
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
