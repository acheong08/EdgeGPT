import httpx, asyncio, aiohttp, ssl, certifi, json, sys
from typing import Generator, Union

from ..conversation import Conversation
from .request import ChatHubRequest
from ..utilities import guess_locale, get_ran_hex, append_identifier
from ..constants import HEADERS, DELIMITER
from ..conversation_style import CONVERSATION_STYLE_TYPE

from BingImageCreator import ImageGenAsync

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


class ChatHub:
    def __init__(
        self,
        conversation: Conversation,
        proxy: str = None,
        cookies: list[dict] | None = None,
    ) -> None:
        self.wss: aiohttp.ClientWebSocketResponse | None = None
        self.request: ChatHubRequest
        self.loop: bool
        self.task: asyncio.Task
        self.request = ChatHubRequest(
            conversation_signature=conversation.struct["conversationSignature"],
            client_id=conversation.struct["clientId"],
            conversation_id=conversation.struct["conversationId"],
        )
        self.cookies = cookies
        self.proxy: str = proxy

    async def ask_stream(
        self,
        prompt: str,
        wss_link: str,
        conversation_style: CONVERSATION_STYLE_TYPE = None,
        raw: bool = False,
        webpage_context: str | None = None,
        search_result: bool = False,
        locale: str = guess_locale(),
    ) -> Generator[bool, Union[dict, str], None]:
        """ """
        timeout = aiohttp.ClientTimeout(total=900)
        self.session = aiohttp.ClientSession(timeout=timeout)

        if self.wss and not self.wss.closed:
            await self.wss.close()
        # Check if websocket is closed
        self.wss = await self.session.ws_connect(
            wss_link,
            headers=HEADERS,
            ssl=ssl_context,
            proxy=self.proxy,
            autoping=False,
        )
        await self._initial_handshake()
        # Construct a ChatHub request
        self.request.update(
            prompt=prompt,
            conversation_style=conversation_style,
            webpage_context=webpage_context,
            search_result=search_result,
            locale=locale,
        )
        # Send request
        await self.wss.send_str(append_identifier(self.request.struct))
        draw = False
        resp_txt = ""
        result_text = ""
        resp_txt_no_link = ""
        while True:
            msg = await self.wss.receive(timeout=900)
            objects = msg.data.split(DELIMITER)
            for obj in objects:
                if obj is None or not obj:
                    continue
                response = json.loads(obj)
                # print(response)
                if response.get("type") != 2 and raw:
                    yield False, response
                elif response.get("type") == 1 and response["arguments"][0].get(
                    "messages",
                ):
                    if not draw:
                        if (
                            response["arguments"][0]["messages"][0].get("messageType")
                            == "GenerateContentQuery"
                        ):
                            async with ImageGenAsync("", True) as image_generator:
                                images = await image_generator.get_images(
                                    response["arguments"][0]["messages"][0]["text"],
                                )
                            for i, image in enumerate(images):
                                resp_txt = f"{resp_txt}\n![image{i}]({image})"
                            draw = True
                        if (
                            response["arguments"][0]["messages"][0]["contentOrigin"]
                            != "Apology"
                        ) and not draw:
                            resp_txt = result_text + response["arguments"][0][
                                "messages"
                            ][0]["adaptiveCards"][0]["body"][0].get("text", "")
                            resp_txt_no_link = result_text + response["arguments"][0][
                                "messages"
                            ][0].get("text", "")
                            if response["arguments"][0]["messages"][0].get(
                                "messageType",
                            ):
                                resp_txt = (
                                    resp_txt
                                    + response["arguments"][0]["messages"][0][
                                        "adaptiveCards"
                                    ][0]["body"][0]["inlines"][0].get("text")
                                    + "\n"
                                )
                                result_text = (
                                    result_text
                                    + response["arguments"][0]["messages"][0][
                                        "adaptiveCards"
                                    ][0]["body"][0]["inlines"][0].get("text")
                                    + "\n"
                                )
                        yield False, resp_txt
                        return

                elif response.get("type") == 2:
                    if response["item"]["result"].get("error"):
                        await self.close()
                        raise Exception(
                            f"{response['item']['result']['value']}: {response['item']['result']['message']}",
                        )
                    if draw:
                        cache = response["item"]["messages"][1]["adaptiveCards"][0][
                            "body"
                        ][0]["text"]
                        response["item"]["messages"][1]["adaptiveCards"][0]["body"][0][
                            "text"
                        ] = (cache + resp_txt)
                    if (
                        response["item"]["messages"][-1]["contentOrigin"] == "Apology"
                        and resp_txt
                    ):
                        response["item"]["messages"][-1]["text"] = resp_txt_no_link
                        response["item"]["messages"][-1]["adaptiveCards"][0]["body"][0][
                            "text"
                        ] = resp_txt
                        print(
                            "Preserved the message from being deleted",
                            file=sys.stderr,
                        )
                    await self.close()
                    yield True, response

    async def _initial_handshake(self) -> None:
        await self.wss.send_str(append_identifier({"protocol": "json", "version": 1}))
        await self.wss.receive(timeout=900)
        await self.wss.send_str(append_identifier({"type": 6}))

    async def close(self) -> None:
        if self.wss and not self.wss.closed:
            await self.wss.close()
        if self.session and not self.session.closed:
            await self.session.close()
