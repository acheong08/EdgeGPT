"""
Main.py
"""
import uuid
import json
import time
import requests
from websocket import WebSocket
from threading import Thread


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
        invocation_id: int,
    ) -> None:
        self.struct: dict

        self.client_id: str = client_id
        self.conversation_id: str = conversation_id
        self.conversation_signature: str = conversation_signature
        self.invocation_id: int = invocation_id
        self.is_start_of_session: bool = True

        self.update(prompt=None, conversation_signature=conversation_signature, client_id=client_id, conversation_id=conversation_id, invocation_id=invocation_id)
    
    def update(
        self,
        prompt: str,
        conversation_signature: str = None,
        client_id: str = None,
        conversation_id: str = None,
        invocation_id: int = None,
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
                    "isStartOfSession": self.is_start_of_session,
                    "message": {
                        "timestamp": "2023-02-09T13:26:58+08:00",
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": prompt,
                        "messageType": "Chat",
                    },
                    "conversationSignature": conversation_signature or self.conversation_signature,
                    "participant": {"id": client_id or self.client_id},
                    "conversationId": conversation_id or self.conversation_id,
                    "previousMessages": [],
                }
            ],
            "invocationId": str(invocation_id),
            "target": "chat",
            "type": 4,
        }
        self.is_start_of_session = False

class Conversation:
    """
    Conversation API
    """

    def __init__(self) -> None:
        self.struct: dict = {'conversationId': None, 'clientId': None, 'conversationSignature': None, 'result': {'value': 'Success', 'message': None}}
        self.__create()

    def __create(self):
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
        cookies = json.loads(
            open("templates/cookies.json", "r", encoding="utf-8").read()
        )
        # Send GET request
        response = requests.get(
            "https://www.bing.com/turing/conversation/create",
            headers=headers,
            cookies=cookies,
            timeout=30,
        )
        # Return response
        self.struct = response.json()


class ChatHub:
    """
    Chat API
    """

    def __init__(self) -> None:
        self.wss = WebSocket()
        self.wss.connect(url="wss://sydney.bing.com/sydney/ChatHub")
        self.__initial_handshake()
        # Ping in another thread
        self.thread = Thread(target=self.__ping)
        self.thread.start()
        self.stop_thread = False
    
    def ask(self, prompt: str):
        pass


    def __initial_handshake(self):
        self.wss.send(append_identifier({"protocol": "json", "version": 1}))
        # Receive blank message
        self.wss.recv()
    
    def __ping(self):
        timing = 10
        while True:
            if timing == 0:
                self.wss.send(append_identifier({"type": 6}))
                # Receive pong
                self.wss.recv()
                timing = 10
            else:
                timing -= 1
            time.sleep(1)
            if self.stop_thread:
                break
    
    def close(self):
        """
        Close all connections
        """
        self.wss.close()
        self.stop_thread = True
        self.thread.join()

async def main():
    """
    Main function
    """
    # Create conversation
    conversation = Conversation()
    print(conversation.struct)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
