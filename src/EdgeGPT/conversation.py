import json
import os
from typing import List
from typing import Union

import httpx

from .constants import HEADERS_INIT_CONVER
from .exceptions import NotAllowedToAccess


class Conversation:
    def __init__(
        self,
        proxy: Union[str, None] = None,
        async_mode: bool = False,
        cookies: Union[List[dict], None] = None,
    ) -> None:
        if async_mode:
            return
        self.struct: dict = {
            "conversationId": None,
            "clientId": None,
            "conversationSignature": None,
            "result": {"value": "Success", "message": None},
        }
        self.proxy = proxy
        proxy = (
            proxy
            or os.environ.get("all_proxy")
            or os.environ.get("ALL_PROXY")
            or os.environ.get("https_proxy")
            or os.environ.get("HTTPS_PROXY")
            or None
        )
        if proxy is not None and proxy.startswith("socks5h://"):
            proxy = "socks5://" + proxy[len("socks5h://") :]
        self.session = httpx.Client(
            proxies=proxy,
            timeout=900,
            headers=HEADERS_INIT_CONVER,
        )
        if cookies:
            for cookie in cookies:
                self.session.cookies.set(cookie["name"], cookie["value"])
        # Send GET request
        response = self.session.get(
            url=os.environ.get("BING_PROXY_URL")
            or "https://edgeservices.bing.com/edgesvc/turing/conversation/create",
        )
        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print(response.text)
            print(response.url)
            raise Exception("Authentication failed")
        try:
            self.struct = response.json()
        except (json.decoder.JSONDecodeError, NotAllowedToAccess) as exc:
            raise Exception(
                "Authentication failed. You have not been accepted into the beta.",
            ) from exc
        if self.struct["result"]["value"] == "UnauthorizedRequest":
            raise NotAllowedToAccess(self.struct["result"]["message"])

    @staticmethod
    async def create(
        proxy: Union[str, None] = None,
        cookies: Union[List[dict], None] = None,
    ) -> "Conversation":
        self = Conversation(async_mode=True)
        self.struct = {
            "conversationId": None,
            "clientId": None,
            "conversationSignature": None,
            "result": {"value": "Success", "message": None},
        }
        self.proxy = proxy
        proxy = (
            proxy
            or os.environ.get("all_proxy")
            or os.environ.get("ALL_PROXY")
            or os.environ.get("https_proxy")
            or os.environ.get("HTTPS_PROXY")
            or None
        )
        if proxy is not None and proxy.startswith("socks5h://"):
            proxy = "socks5://" + proxy[len("socks5h://") :]
        transport = httpx.AsyncHTTPTransport(retries=900)
        # Convert cookie format to httpx format
        formatted_cookies = None
        if cookies:
            formatted_cookies = httpx.Cookies()
            for cookie in cookies:
                formatted_cookies.set(cookie["name"], cookie["value"])
        async with httpx.AsyncClient(
            proxies=proxy,
            timeout=30,
            headers=HEADERS_INIT_CONVER,
            transport=transport,
            cookies=formatted_cookies,
        ) as client:
            # Send GET request
            response = await client.get(
                url=os.environ.get("BING_PROXY_URL")
                or "https://www.bing.com/turing/conversation/create",
                follow_redirects=True,
            )
        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print(response.text)
            print(response.url)
            raise Exception("Authentication failed")
        try:
            self.struct = response.json()
        except (json.decoder.JSONDecodeError, NotAllowedToAccess) as exc:
            print(response.text)
            raise Exception(
                "Authentication failed. You have not been accepted into the beta.",
            ) from exc
        if self.struct["result"]["value"] == "UnauthorizedRequest":
            raise NotAllowedToAccess(self.struct["result"]["message"])
        return self
