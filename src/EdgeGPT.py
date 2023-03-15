"""
Main.py
"""
from __future__ import annotations
import argparse
import asyncio
import json
import os
import random
import sys
import uuid
from enum import Enum
from typing import Generator
from typing import Literal
from typing import Optional
from typing import Union

import httpx
import websockets.client as websockets

DELIMITER = "\x1e"


# Generate random IP between range 13.104.0.0/14
FORWARDED_IP = (
    f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
)

HEADERS = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": '"Not_A Brand";v="99", "Microsoft Edge";v="110", "Chromium";v="110"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"109.0.1518.78"',
    'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.192", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.69"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"15.0.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-ms-client-request-id": str(uuid.uuid4()),
    "x-ms-useragent": "azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.10.0 OS/Win32",
    "Referer": "https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx",
    "Referrer-Policy": "origin-when-cross-origin",
    "x-forwarded-for": FORWARDED_IP,
}

HEADERS_INIT_CONVER = {
    'authority': 'edgeservices.bing.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    "accept-language": "en-US,en;q=0.9",
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"110.0.1587.69"',
    'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.192", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.69"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    'x-edge-shopping-flag': '1',
}   

class NotAllowedToAccess(Exception):
    pass


class ConversationStyle(Enum):
    creative = "h3imaginative"
    balanced = "harmonyv3"
    precise = "h3precise"


CONVERSATION_STYLE_TYPE = Optional[
    Union[ConversationStyle, Literal["creative", "balanced", "precise"]]
]


def append_identifier(msg: dict) -> str:
    """
    Appends special character to end of message to identify end of message
    """
    # Convert dict to json string
    return json.dumps(msg) + DELIMITER


class ChatHubRequest:
    """
    Request object for ChatHub
    """

    def __init__(
        self,
        conversation_signature: str,
        client_id: str,
        conversation_id: str,
        invocation_id: int = 0,
    ) -> None:
        self.struct: dict = {}

        self.client_id: str = client_id
        self.conversation_id: str = conversation_id
        self.conversation_signature: str = conversation_signature
        self.invocation_id: int = invocation_id

    def update(
        self,
        prompt: str,
        conversation_style: CONVERSATION_STYLE_TYPE,
        options: Optional[list] = None,
    ) -> None:
        """
        Updates request object
        """
        if options is None:
            options = [
                "deepleo",
                "enable_debug_commands",
                "disable_emoji_spoken_text",
                "enablemm",
            ]
        if conversation_style:
            if not isinstance(conversation_style, ConversationStyle):
                conversation_style = getattr(ConversationStyle, conversation_style)
            options = [
                "deepleo",
                "enable_debug_commands",
                "disable_emoji_spoken_text",
                "enablemm",
                conversation_style.value,
            ]
        self.struct = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": options,
                    "isStartOfSession": self.invocation_id == 0,
                    "message": {
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": prompt,
                        "messageType": "Chat",
                    },
                    "conversationSignature": self.conversation_signature,
                    "participant": {
                        "id": self.client_id,
                    },
                    "conversationId": self.conversation_id,
                },
            ],
            "invocationId": str(self.invocation_id),
            "target": "chat",
            "type": 4,
        }
        self.invocation_id += 1


class Conversation:
    """
    Conversation API
    """

    def __init__(self, cookiePath: str = "", cookies: Optional[dict] = None) -> None:
        self.struct: dict = {
            "conversationId": None,
            "clientId": None,
            "conversationSignature": None,
            "result": {"value": "Success", "message": None},
        }
        self.session = httpx.Client()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            },
        )
        if cookies is not None:
            cookie_file = cookies
        else:
            f = (
                open(cookiePath, encoding="utf8").read()
                if cookiePath
                else open(os.environ.get("COOKIE_FILE"), encoding="utf-8").read()
            )
            cookie_file = json.loads(f)
        for cookie in cookie_file:
            self.session.cookies.set(cookie["name"], cookie["value"])
        url = "https://edgeservices.bing.com/edgesvc/turing/conversation/create"
        # Send GET request
        response = self.session.get(
            url,
            timeout=30,
            headers=HEADERS_INIT_CONVER,
        )
        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print(response.text)
            raise Exception("Authentication failed")
        try:
            self.struct = response.json()
            if self.struct["result"]["value"] == "UnauthorizedRequest":
                raise NotAllowedToAccess(self.struct["result"]["message"])
        except (json.decoder.JSONDecodeError, NotAllowedToAccess) as exc:
            raise Exception(
                "Authentication failed. You have not been accepted into the beta.",
            ) from exc


class ChatHub:
    """
    Chat API
    """

    def __init__(self, conversation: Conversation) -> None:
        self.wss: Optional[websockets.WebSocketClientProtocol] = None
        self.request: ChatHubRequest
        self.loop: bool
        self.task: asyncio.Task
        self.request = ChatHubRequest(
            conversation_signature=conversation.struct["conversationSignature"],
            client_id=conversation.struct["clientId"],
            conversation_id=conversation.struct["conversationId"],
        )

    async def ask_stream(
        self,
        prompt: str,
        conversation_style: CONVERSATION_STYLE_TYPE = None,
    ) -> Generator[str, None, None]:
        """
        Ask a question to the bot
        """
        # Check if websocket is closed
        if self.wss and self.wss.closed or not self.wss:
            self.wss = await websockets.connect(
                "wss://sydney.bing.com/sydney/ChatHub",
                extra_headers=HEADERS,
                max_size=None,
            )
            await self.__initial_handshake()
        # Construct a ChatHub request
        self.request.update(prompt=prompt, conversation_style=conversation_style)
        # Send request
        await self.wss.send(append_identifier(self.request.struct))
        final = False
        while not final:
            objects = str(await self.wss.recv()).split(DELIMITER)
            for obj in objects:
                if obj is None or obj == "":
                    continue
                response = json.loads(obj)
                if response.get("type") == 1 and response["arguments"][0].get("messages"):
                    yield False, response["arguments"][0]["messages"][0][
                        "adaptiveCards"
                    ][0]["body"][0]["text"]
                elif response.get("type") == 2:
                    final = True
                    yield True, response

    async def __initial_handshake(self):
        await self.wss.send(append_identifier({"protocol": "json", "version": 1}))
        await self.wss.recv()

    async def close(self):
        """
        Close the connection
        """
        if self.wss and not self.wss.closed:
            await self.wss.close()


class Chatbot:
    """
    Combines everything to make it seamless
    """

    def __init__(self, cookiePath: str = "", cookies: Optional[dict] = None) -> None:
        self.cookiePath: str = cookiePath
        self.cookies: Optional[dict] = cookies
        self.chat_hub: ChatHub = ChatHub(Conversation(self.cookiePath, self.cookies))

    async def ask(
        self,
        prompt: str,
        conversation_style: CONVERSATION_STYLE_TYPE = None,
    ) -> dict:
        """
        Ask a question to the bot
        """
        async for final, response in self.chat_hub.ask_stream(
            prompt=prompt,
            conversation_style=conversation_style,
        ):
            if final:
                return response
        self.chat_hub.wss.close()

    async def ask_stream(
        self,
        prompt: str,
        conversation_style: CONVERSATION_STYLE_TYPE = None,
    ) -> Generator[str, None, None]:
        """
        Ask a question to the bot
        """
        async for response in self.chat_hub.ask_stream(
            prompt=prompt,
            conversation_style=conversation_style,
        ):
            yield response

    async def close(self):
        """
        Close the connection
        """
        await self.chat_hub.close()

    async def reset(self):
        """
        Reset the conversation
        """
        await self.close()
        self.chat_hub = ChatHub(Conversation(self.cookiePath, self.cookies))


def get_input(prompt):
    """
    Multi-line input function
    """
    # Display the prompt
    print(prompt, end="")

    if args.enter_once:
        user_input = input()
        print()
        return user_input

    # Initialize an empty list to store the input lines
    lines = []

    # Read lines of input until the user enters an empty line
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    # Join the lines, separated by newlines, and store the result
    user_input = "\n".join(lines)

    # Return the input
    return user_input


async def main():
    """
    Main function
    """
    print("Initializing...")
    bot = Chatbot()
    while True:
        prompt = get_input("\nYou:\n")
        if prompt == "!exit":
            break
        elif prompt == "!help":
            print(
                """
            !help - Show this help message
            !exit - Exit the program
            !reset - Reset the conversation
            """,
            )
            continue
        elif prompt == "!reset":
            await bot.reset()
            continue
        print("Bot:")
        if args.no_stream:
            print(
                (await bot.ask(prompt=prompt, conversation_style=args.style))["item"][
                    "messages"
                ][1]["adaptiveCards"][0]["body"][0]["text"],
            )
        else:
            wrote = 0
            async for final, response in bot.ask_stream(
                prompt=prompt,
                conversation_style=args.style,
            ):
                if not final:
                    print(response[wrote:], end="")
                    wrote = len(response)
                    sys.stdout.flush()
            print()
        sys.stdout.flush()
    await bot.close()


if __name__ == "__main__":
    print(
        """
        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit
        Enter twice to send message or set --enter-once to send one line message
    """,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--enter-once", action="store_true")
    parser.add_argument("--no-stream", action="store_true")
    parser.add_argument(
        "--style",
        choices=["creative", "balanced", "precise"],
        default="balanced",
    )
    parser.add_argument(
        "--cookie-file",
        type=str,
        default="cookies.json",
        required=True,
    )
    args = parser.parse_args()
    os.environ["COOKIE_FILE"] = args.cookie_file
    args = parser.parse_args()
    asyncio.run(main())
