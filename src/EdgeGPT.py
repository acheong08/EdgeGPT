"""
Main.py
"""
import asyncio
import json
import os
import uuid
import sys

import requests
import websockets.client as websockets


def append_identifier(msg: dict) -> str:
    """
    Appends special character to end of message to identify end of message
    """
    # Convert dict to json string
    return json.dumps(msg) + ""


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
        self.struct: dict

        self.client_id: str = client_id
        self.conversation_id: str = conversation_id
        self.conversation_signature: str = conversation_signature
        self.invocation_id: int = invocation_id

    def update(
        self,
        prompt: str,
    ) -> None:
        """
        Updates request object
        """
        self.struct = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": [
                        "nlu_direct_response_filter",
                        "deepleo",
                        "enable_debug_commands",
                        "disable_emoji_spoken_text",
                        "responsible_ai_policy_235",
                        "enablemm",
                    ],
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

    def __init__(self) -> None:
        self.struct: dict = {
            "conversationId": None,
            "clientId": None,
            "conversationSignature": None,
            "result": {"value": "Success", "message": None},
        }
        # Build request
        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "sec-ch-ua": '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-full-version": '"111.0.1652.0"',
            "sec-ch-ua-full-version-list": '"Microsoft Edge";v="111.0.1652.0", "Not(A:Brand";v="8.0.0.0", "Chromium";v="111.0.5551.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "",
            "sec-ch-ua-platform": '"Linux"',
            "sec-ch-ua-platform-version": '"5.19.0"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.0.0",
            "x-ms-client-request-id": str(uuid.uuid4()),
            "x-ms-useragent": "azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.10.0 OS/Linuxx86_64",
        }
        # Create cookies
        cookies = {
            "_U": os.environ.get("BING_U") or sys.argv[1],
        }
        # Send GET request
        response = requests.get(
            "https://www.bing.com/turing/conversation/create",
            headers=headers,
            cookies=cookies,
            timeout=30,
        )
        if response.status_code != 200:
            raise Exception("Authentication failed")
        # Return response
        try:
            self.struct = response.json()
        except json.decoder.JSONDecodeError:
            raise Exception("Authentication failed. You have not been accepted into the beta.") from json.decoder.JSONDecodeError


class ChatHub:
    """
    Chat API
    """

    def __init__(self) -> None:
        self.wss: websockets.WebSocketClientProtocol
        self.request: ChatHubRequest
        self.loop: bool
        self.task: asyncio.Task

    async def init(self, conversation: Conversation) -> None:
        """
        Separate initialization to allow async
        """
        self.wss = await websockets.connect("wss://sydney.bing.com/sydney/ChatHub")
        self.request = ChatHubRequest(
            conversation_signature=conversation.struct["conversationSignature"],
            client_id=conversation.struct["clientId"],
            conversation_id=conversation.struct["conversationId"],
        )
        self.loop = True
        await self.__initial_handshake()

        # Make async ping loop (long running)
        self.task = asyncio.create_task(self.__ping())

    async def ask(self, prompt: str) -> dict:
        """
        Ask a question to the bot
        """
        # Construct a ChatHub request
        self.request.update(prompt=prompt)
        # Send request
        await self.wss.send(append_identifier(self.request.struct))
        while True:
            objects = str(await self.wss.recv()).split("")
            for obj in objects:
                if obj is None or obj == "":
                    continue
                response = json.loads(obj)
                if response.get("type") == 2:
                    return response

    async def __initial_handshake(self):
        await self.wss.send(append_identifier({"protocol": "json", "version": 1}))
        await self.wss.recv()
        await self.wss.send(append_identifier({"type": 6}))
        await self.wss.recv()

    async def __ping(self):
        while self.loop:
            try:
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                break
            await self.wss.send(append_identifier({"type": 6}))
            await self.wss.recv()

    async def close(self):
        """
        Close the connection
        """
        self.loop = False
        await self.wss.close()
        self.task.cancel()


class Chatbot:
    """
    Combines everything to make it seamless
    """

    def __init__(self) -> None:
        self.conversation: Conversation
        self.chat_hub: ChatHub

    async def start(self) -> None:
        """
        Separate initialization to allow async
        """
        self.conversation = Conversation()
        self.chat_hub = ChatHub()
        await self.chat_hub.init(conversation=self.conversation)

    async def ask(self, prompt: str) -> dict:
        """
        Ask a question to the bot
        """
        return await self.chat_hub.ask(prompt=prompt)

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
        await self.start()


def get_input(prompt):
    """
    Multi-line input function
    """
    # Display the prompt
    print(prompt, end="")

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
    await bot.start()
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
            """
            )
            continue
        elif prompt == "!reset":
            await bot.reset()
            continue
        print("Bot:")
        print(
            (await bot.ask(prompt=prompt))["item"]["messages"][1]["adaptiveCards"][0][
                "body"
            ][0]["text"]
        )
    await bot.close()


if __name__ == "__main__":
    print(
        """
        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit
        Enter twice to send message
    """
    )
    asyncio.run(main())
