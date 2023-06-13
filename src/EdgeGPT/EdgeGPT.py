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
                json.dumps(
                    {
                        "conversation_id": conversation_id,
                        "conversation_signature": conversation_signature,
                        "client_id": client_id,
                        "invocation_id": invocation_id,
                    }
                ),
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

    async def get_activity(self) -> dict:
        """
        Gets the recent activity (requires cookies)
        """
        return await self.chat_hub.get_activity()

    async def ask(
        self,
        prompt: str,
        wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
        conversation_style: CONVERSATION_STYLE_TYPE = None,
        webpage_context: str | None = None,
        search_result: bool = False,
        locale: str = guess_locale(),
        simplify_response: bool = False,
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
                if not simplify_response:
                    return response
                message = response["item"]["messages"][-1]
                return {
                    "text": message["text"],
                    "author": message["author"],
                    "sources": message["sourceAttributions"],
                    "sources_text": message["adaptiveCards"][0]["body"][-1]["text"],
                    "suggestions": [
                        suggestion["text"]
                        for suggestion in message["suggestedResponses"]
                    ],
                    "messages_left": response["item"]["throttling"][
                        "maxNumUserMessagesInConversation"
                    ]
                    - response["item"]["throttling"][
                        "numUserMessagesInConversation"
                    ],
                    "adaptive_text": message["adaptiveCards"][0]["body"][0]["text"],
                }
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


if __name__ == "__main__":
    from .main import main

    main()
