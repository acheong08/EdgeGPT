import asyncio
import json
import platform
import time
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Union

from EdgeGPT.EdgeGPT import Chatbot
from EdgeGPT.EdgeGPT import ConversationStyle
from EdgeGPT.ImageGen import ImageGen


class Cookie:
    """
    Convenience class for Bing Cookie files, data, and configuration. This Class
    is updated dynamically by the Query class to allow cycling through >1
    cookie/credentials file e.g. when daily request limits (current 200 per
    account per day) are exceeded.
    """

    current_file_index = 0
    dirpath = Path("./").resolve()
    search_pattern = "bing_cookies_*.json"
    ignore_files = set()
    current_filepath: Union[dict, None] = None

    @classmethod
    def fetch_default(cls, path: Union[Path, None] = None) -> None:
        from selenium import webdriver
        from selenium.webdriver.common.by import By

        driver = webdriver.Edge()
        driver.get("https://bing.com/chat")
        time.sleep(5)
        xpath = '//button[@id="bnp_btn_accept"]'
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(2)
        xpath = '//a[@id="codexPrimaryButton"]'
        driver.find_element(By.XPATH, xpath).click()
        if path is None:
            path = Path("./bing_cookies__default.json")
            # Double underscore ensures this file is first when sorted
        cookies = driver.get_cookies()
        Path(path).write_text(json.dumps(cookies, indent=4), encoding="utf-8")
        # Path again in case supplied path is: str
        print(f"Cookies saved to: {path}")
        driver.quit()

    @classmethod
    def files(cls) -> List[Path]:
        """Return a sorted list of all cookie files matching .search_pattern"""
        all_files = set(cls.dirpath.glob(cls.search_pattern))
        return sorted(all_files - cls.ignore_files)

    @classmethod
    def import_data(cls) -> None:
        """
        Read the active cookie file and populate the following attributes:

          .current_filepath
          .current_data
          .image_token
        """
        try:
            cls.current_filepath = cls.files()[cls.current_file_index]
        except IndexError as exc:
            print(
                "> Please set Cookie.current_filepath to a valid cookie file, then run Cookie.import_data()",
            )
            raise "No valid cookie file found." from exc
        print(f"> Importing cookies from: {cls.current_filepath.name}")
        with Path.open(cls.current_filepath, encoding="utf-8") as file:
            cls.current_data = json.load(file)
        cls.image_token = [x for x in cls.current_data if x.get("name") == "_U"]
        cls.image_token = cls.image_token[0].get("value")

    @classmethod
    def import_next(cls) -> None:
        """
        Cycle through to the next cookies file.  Import it.  Mark the previous
        file to be ignored for the remainder of the current session.
        """
        cls.ignore_files.add(cls.current_filepath)
        if Cookie.current_file_index >= len(cls.files()):
            Cookie.current_file_index = 0
        Cookie.import_data()


class Query:
    """
    A convenience class that wraps around EdgeGPT.Chatbot to encapsulate input,
    config, and output all together.  Relies on Cookie class for authentication
    """

    def __init__(
        self,
        prompt: str,
        style: str = "precise",
        content_type: str = "text",
        cookie_file: int = 0,
        echo: bool = True,
        echo_prompt: bool = False,
        proxy: Union[str, None] = None,
    ) -> None:
        """
        Arguments:

        prompt: Text to enter into Bing Chat
        style: creative, balanced, or precise
        content_type: "text" for Bing Chat; "image" for Dall-e
        cookie_file: Path, filepath string, or index (int) to list of cookie paths
        echo: Print something to confirm request made
        echo_prompt: Print confirmation of the evaluated prompt
        """
        self.proxy = proxy
        self.index = []
        self.request_count = {}
        self.image_dirpath = Path("./").resolve()
        Cookie.import_data()
        self.index += [self]
        self.prompt = prompt
        files = Cookie.files()
        if isinstance(cookie_file, int):
            index = cookie_file if cookie_file < len(files) else 0
        else:
            if not isinstance(cookie_file, (str, Path)):
                message = "'cookie_file' must be an int, str, or Path object"
                raise TypeError(message)
            cookie_file = Path(cookie_file)
            if cookie_file in files:  # Supplied filepath IS in Cookie.dirpath
                index = files.index(cookie_file)
            else:  # Supplied filepath is NOT in Cookie.dirpath
                if cookie_file.is_file():
                    Cookie.dirpath = cookie_file.parent.resolve()
                if cookie_file.is_dir():
                    Cookie.dirpath = cookie_file.resolve()
                index = 0
        Cookie.current_file_index = index
        if content_type == "text":
            self.style = style
            self.log_and_send_query(echo, echo_prompt)
        if content_type == "image":
            self.create_image()

    def log_and_send_query(self, echo: bool, echo_prompt: bool) -> None:
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.response = asyncio.run(self.send_to_bing(echo, echo_prompt))
        name = str(Cookie.current_filepath.name)
        if not self.request_count.get(name):
            self.request_count[name] = 1
        else:
            self.request_count[name] += 1

    def create_image(self) -> None:
        image_generator = ImageGen(Cookie.image_token)
        image_generator.save_images(
            image_generator.get_images(self.prompt),
            output_dir=self.image_dirpath,
        )

    async def send_to_bing(self, echo: bool = True, echo_prompt: bool = False) -> str:
        """Creat, submit, then close a Chatbot instance.  Return the response"""
        retries = len(Cookie.files())
        while retries:
            try:
                # Read the cookies file
                bot = await Chatbot.create(
                    proxy=self.proxy,
                    cookies=Cookie.current_data,
                )
                if echo_prompt:
                    print(f"> {self.prompt}=")
                if echo:
                    print("> Waiting for response...")
                if self.style.lower() not in "creative balanced precise".split():
                    self.style = "precise"
                return await bot.ask(
                    prompt=self.prompt,
                    conversation_style=getattr(ConversationStyle, self.style),
                    # wss_link="wss://sydney.bing.com/sydney/ChatHub"
                    # What other values can this parameter take? It seems to be optional
                )
            except KeyError:
                print(
                    f"> KeyError [{Cookie.current_filepath.name} may have exceeded the daily limit]",
                )
                Cookie.import_next()
                retries -= 1
            finally:
                await bot.close()
        return None

    @property
    def output(self) -> str:
        """The response from a completed Chatbot request"""
        return self.response["item"]["messages"][1]["text"]

    @property
    def sources(self) -> str:
        """The source names and details parsed from a completed Chatbot request"""
        return self.response["item"]["messages"][1]["sourceAttributions"]

    @property
    def sources_dict(self) -> Dict[str, str]:
        """The source names and details as a dictionary"""
        sources_dict = {}
        name = "providerDisplayName"
        url = "seeMoreUrl"
        for source in self.sources:
            if name in source and url in source:
                sources_dict[source[name]] = source[url]
            else:
                continue
        return sources_dict

    @property
    def code(self) -> str:
        """Extract and join any snippets of Python code in the response"""
        code_blocks = self.output.split("```")[1:-1:2]
        code_blocks = ["\n".join(x.splitlines()[1:]) for x in code_blocks]
        return "\n\n".join(code_blocks)

    @property
    def languages(self) -> Set[str]:
        """Extract all programming languages given in code blocks"""
        code_blocks = self.output.split("```")[1:-1:2]
        return {x.splitlines()[0] for x in code_blocks}

    @property
    def suggestions(self) -> List[str]:
        """Follow-on questions suggested by the Chatbot"""
        return [
            x["text"]
            for x in self.response["item"]["messages"][1]["suggestedResponses"]
        ]

    def __repr__(self) -> str:
        return f"<EdgeGPT.Query: {self.prompt}>"

    def __str__(self) -> str:
        return self.output


class ImageQuery(Query):
    def __init__(self, prompt: str, **kwargs) -> None:
        kwargs["content_type"] = "image"
        super().__init__(prompt, **kwargs)

    def __repr__(self) -> str:
        return f"<EdgeGPT.ImageQuery: {self.prompt}>"
