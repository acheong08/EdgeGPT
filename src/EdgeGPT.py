"""
Main.py
"""
import argparse
import asyncio
import json
import os
import sys

import requests
import websockets.client as websockets

DELIMITER = "\x1e"


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
        # Create cookies
        if os.environ.get("BING_U") is None:
            home = os.path.expanduser("~")
            # Check if token exists
            token_path = f"{home}/.config/bing_token"
            # Make .config directory if it doesn't exist
            if not os.path.exists(f"{home}/.config"):
                os.mkdir(f"{home}/.config")
            if os.path.exists(token_path):
                with open(token_path, "r", encoding="utf-8") as file:
                    token = file.read()
            else:
                # POST request to get token
                url = "https://images.duti.tech/allow"
                response = requests.post(url, timeout=10)
                if response.status_code != 200:
                    raise Exception("Authentication failed")
                token = response.json()["token"]
                # Save token
                with open(token_path, "w", encoding="utf-8") as file:
                    file.write(token)
            headers = {
                "Authorization": token,
            }
            url = "https://images.duti.tech/auth"
            # Send GET request
            response = requests.get(
                url,
                headers=headers,
                timeout=10,
            )
            if response.status_code != 200:
                raise Exception("Authentication failed")

        else:
            cookies = {
                "_U": os.environ.get("BING_U"),
            }
            url = "https://www.bing.com/turing/conversation/create"
            # Send GET request
            response = requests.get(
                url,
                cookies=cookies,
                timeout=30,
            )
            if response.status_code != 200:
                raise Exception("Authentication failed")
        try:
            self.struct = response.json()
        except json.decoder.JSONDecodeError as exc:
            raise Exception(
                "Authentication failed. You have not been accepted into the beta.",
            ) from exc


class ChatHub:
    """
    Chat API
    """

    def __init__(self, conversation: Conversation) -> None:
        self.wss: websockets.WebSocketClientProtocol = None
        self.request: ChatHubRequest
        self.loop: bool
        self.task: asyncio.Task
        self.request = ChatHubRequest(
            conversation_signature=conversation.struct["conversationSignature"],
            client_id=conversation.struct["clientId"],
            conversation_id=conversation.struct["conversationId"],
        )

    async def ask_stream(self, prompt: str) -> str:
        """
        Ask a question to the bot
        """
        # Check if websocket is closed
        if self.wss:
            if self.wss.closed:
                self.wss = await websockets.connect(
                    "wss://sydney.bing.com/sydney/ChatHub",
                )
                await self.__initial_handshake()
        else:
            self.wss = await websockets.connect("wss://sydney.bing.com/sydney/ChatHub")
            await self.__initial_handshake()
        # Construct a ChatHub request
        self.request.update(prompt=prompt)
        # Send request
        await self.wss.send(append_identifier(self.request.struct))
        final = False
        while not final:
            objects = str(await self.wss.recv()).split(DELIMITER)
            for obj in objects:
                if obj is None or obj == "":
                    continue
                response = json.loads(obj)
                if response.get("type") == 1:
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
        if self.wss:
            if not self.wss.closed:
                await self.wss.close()


class Chatbot:
    """
    Combines everything to make it seamless
    """

    def __init__(self) -> None:
        self.chat_hub: ChatHub = ChatHub(Conversation())

    async def ask(self, prompt: str) -> dict:
        """
        Ask a question to the bot
        """
        async for final, response in self.chat_hub.ask_stream(prompt=prompt):
            if final:
                return response

    async def ask_stream(self, prompt: str) -> str:
        """
        Ask a question to the bot
        """
        async for response in self.chat_hub.ask_stream(prompt=prompt):
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
        self.chat_hub = ChatHub(Conversation())


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
                (await bot.ask(prompt=prompt))["item"]["messages"][1]["adaptiveCards"][
                    0
                ]["body"][0]["text"],
            )
        else:
            wrote = 0
            async for final, response in bot.ask_stream(prompt=prompt):
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
        Enter twice to send message
    """,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-stream", action="store_true")
    parser.add_argument("--bing-cookie", type=str, default="")
    args = parser.parse_args()
    if args.bing_cookie:
        os.environ["BING_U"] = args.bing_cookie
    asyncio.run(main())
