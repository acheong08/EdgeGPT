import asyncio
import contextlib
import json
import re
from pathlib import Path

from log2d import Log

from .EdgeGPT import Chatbot, ConversationStyle
from .ImageGen import ImageGen

Log("BingChat")
log = Log.BingChat.debug  # shortcut to create a log entry


class Cookie:
    """
    Convenience class for Bing Cookie files, data, and configuration. This Class
    is updated dynamically by the Query class to allow cycling through >1
    cookie/credentials file e.g. when daily request limits (current 200 per
    account per day) are exceeded.
    """

    current_file_index = 0
    dir_path = Path.home().resolve() / "bing_cookies"
    current_file_path = dir_path  # Avoid Path errors when no cookie file used
    search_pattern = "bing_cookies_*.json"
    ignore_files = set()
    request_count = {}
    supplied_files = set()
    rotate_cookies = True

    @classmethod
    def files(cls: type) -> list[Path]:
        """
        Return a sorted list of all cookie files matching .search_pattern in
        cls.dir_path, plus any supplied files, minus any ignored files.
        """
        all_files = set(Path(cls.dir_path).glob(cls.search_pattern))
        if hasattr(cls, "supplied_files"):
            supplied_files = {x for x in cls.supplied_files if x.is_file()}
            all_files.update(supplied_files)
        return sorted(all_files - cls.ignore_files)

    @classmethod
    def import_data(cls: type) -> None:
        """
        Read the active cookie file and populate the following attributes:

          .current_file_path
          .current_data
          .image_token
        """
        if not cls.files():
            log("No files in Cookie.dir_path")
            return
        try:
            cls.current_file_path = cls.files()[cls.current_file_index]
        except IndexError:
            log(f"Invalid file index [{cls.current_file_index}]")
            log("Files in Cookie.dir_path:")
            for file in cls.files():
                log(f"{file}")
            return
        log(f"Importing cookies from: {cls.current_file_path.name}")
        with open(cls.current_file_path, encoding="utf-8") as file:
            cls.current_data = json.load(file)
        cls.image_token = [
            x for x in cls.current_data if x.get("name").startswith("_U")
        ]
        cls.image_token = cls.image_token[0].get("value")

    @classmethod
    def import_next(cls: type, discard: bool = False) -> None:
        """
        Cycle through to the next cookies file then import it.

        discard (bool): True -Mark the previous file to be ignored for the remainder of the current session.  Otherwise cycle through all available
        cookie files (sharing the workload and 'resting' when not in use).
        """
        if not hasattr(cls, "current_file_path"):
            cls.import_data()
            return
        with contextlib.suppress(AttributeError):
            # Will fail on first instantiation because no current_file_path
            if discard:
                cls.ignore_files.add(cls.current_file_path)
            else:
                Cookie.current_file_index += 1
        if Cookie.current_file_index >= len(cls.files()):
            Cookie.current_file_index = 0
        Cookie.import_data()


class Query:
    """
    A convenience class that wraps around EdgeGPT.Chatbot to encapsulate input,
    config, and output all together.  Relies on Cookie class for authentication
    unless ignore_cookies=True
    """

    index = []
    image_dir_path = Path.cwd().resolve() / "bing_images"

    def __init__(
        self,
        prompt: str,
        style: ConversationStyle = "precise",
        content_type: str = "text",
        cookie_files: set[Path] = None,
        ignore_cookies: bool = False,
        echo: bool = True,
        echo_prompt: bool = False,
        locale: str = "en-GB",
        simplify_response: bool = True,
    ) -> None:
        """
        Arguments:

        prompt: Text to enter into Bing Chat
        style: creative, balanced, or precise
        content_type: "text" for Bing Chat; "image" for Dall-e
        ignore_cookies (bool): Ignore cookie data altogether
        echo: Print something to confirm request made
        echo_prompt: Print confirmation of the evaluated prompt
        simplify_response: True -> single simplified prompt/response exchange
        cookie_files: iterable of Paths or strings of cookie files (json)

        Files in Cookie.dir_path will also be used if they exist.  This defaults
        to the current working directory, so set Cookie.dir_path before
        creating a Query if your cookie files are elsewhere.
        """
        self.__class__.index += [self]
        self.prompt = prompt
        self.locale = locale
        self.simplify_response = simplify_response
        self.ignore_cookies = ignore_cookies
        if not ignore_cookies:
            if cookie_files:
                # Convert singular argument to an iterable:
                if isinstance(cookie_files, (str, Path)):
                    cookie_files = {cookie_files}
                # Check all elements exist and are Paths:
                cookie_files = {
                    Path(x).resolve()
                    for x in cookie_files
                    if isinstance(x, (str, Path)) and x
                }
                Cookie.supplied_files = cookie_files
            files = Cookie.files()  # includes .supplied_files
            if Cookie.rotate_cookies:
                Cookie.import_next()
            else:
                Cookie.import_data()
        if content_type == "text":
            self.style = style
            self.log_and_send_query(echo, echo_prompt)
        if content_type == "image":
            self.create_image()

    def log_and_send_query(self, echo: bool, echo_prompt: bool) -> None:
        self.response = asyncio.run(self.send_to_bing(echo, echo_prompt))
        if not hasattr(Cookie, "current_data"):
            name = "<no_cookies>"
        else:
            name = Cookie.current_file_path.name
        if not Cookie.request_count.get(name):
            Cookie.request_count[name] = 1
        else:
            Cookie.request_count[name] += 1

    def create_image(self) -> None:
        image_generator = ImageGen(Cookie.image_token)
        image_generator.save_images(
            image_generator.get_images(self.prompt),
            output_dir=self.__class__.image_dir_path,
        )

    async def send_to_bing(self, echo: bool = True, echo_prompt: bool = False) -> str:
        """Creat, submit, then close a Chatbot instance.  Return the response"""
        retries = len(Cookie.files()) or 1
        while retries:
            if not hasattr(Cookie, "current_data"):
                bot = await Chatbot.create()
            else:
                bot = await Chatbot.create(cookies=Cookie.current_data)
            if echo_prompt:
                log(f"{self.prompt=}")
            if echo:
                log("Waiting for response...")
            if self.style.lower() not in "creative balanced precise".split():
                self.style = "precise"
            try:
                return await bot.ask(
                    prompt=self.prompt,
                    conversation_style=getattr(ConversationStyle, self.style),
                    simplify_response=self.simplify_response,
                    locale=self.locale,
                )
            except Exception as ex:
                log(
                    f"Exception: [{Cookie.current_file_path.name} may have exceeded the daily limit]\n{ex}",
                )
                Cookie.import_next(discard=True)
                retries -= 1
            finally:
                await bot.close()
        return None

    @property
    def output(self) -> str:
        """The response from a completed Chatbot request"""
        if not self.simplify_response:
            return [
                x.get("text") or x.get("hiddenText")
                for x in self.response["item"]["messages"]
                if x["author"] == "bot"
            ]
        try:
            return self.response["text"]
        except TypeError as te:
            raise TypeError(
                f"{te}\n(No response received - probably rate throttled...)"
            ) from te

    @property
    def sources(self) -> list[list[dict]]:
        """The source names and details parsed from a completed Chatbot request"""
        if self.simplify_response:
            return self.response["sources_text"]
        return [
            x.get("sourceAttributions") or []
            for x in self.response["item"]["messages"]
            if x["author"] == "bot"
        ]

    @property
    def sources_dict(self) -> dict[int, str]:
        """The source names and details as a dictionary"""
        if self.simplify_response:
            text = self.response["sources_text"]
            sources = enumerate(re.findall(r"\((http.*?)\)", text))
            return {index + 1: value for index, value in sources}
        all_sources = []
        name = "providerDisplayName"
        url = "seeMoreUrl"
        for sources in self.sources:
            if not sources:
                continue
            data = {
                index + 1: source[url]
                for index, source in enumerate(sources)
                if name in source and url in source
            }
            all_sources += [data]
        return all_sources

    @property
    def code_block_formats(self) -> list[str]:
        """
        Extract a list of programming languages/formats used in code blocks
        """
        regex = r"``` *(\b\w+\b\+*) *"
        if self.simplify_response:
            return re.findall(regex, self.output)
        return re.findall(regex, "\n".join(self.output))

    @property
    def code_blocks(self) -> list[str]:
        """
        Return a list of code blocks (```) or snippets (`) as strings.

        If the response contains a mix of snippets and code blocks, return the
        code blocks only.

        This method is not suitable if the main text response includes either of
        the delimiters but not as part of an actual snippet or code block.

        For example:
        'In Markdown, the back-tick (`) is used to denote a code snippet'

        """

        final_blocks = []
        if isinstance(self.output, str):  # I.e. simplify_response is True
            separator = "```" if "```" in self.output else "`"
            code_blocks = self.output.split(separator)[1:-1:2]
            if separator == "`":
                return code_blocks
        else:
            code_blocks = []
            for response in self.output:
                separator = "```" if "```" in response else "`"
                code_blocks.extend(response.split(separator)[1:-1:2])
            code_blocks = [x for x in code_blocks if x]
        # Remove language name if present:
        for block in code_blocks:
            lines = block.splitlines()
            code = lines[1:] if re.match(" *\\w+ *", lines[0]) else lines
            final_blocks += ["\n".join(code).removeprefix(separator)]
        return [x for x in final_blocks if x]

    @property
    def code(self) -> str:
        """
        Extract and join any snippets of code or formatted data in the response
        """
        return "\n\n".join(self.code_blocks)

    @property
    def suggestions(self) -> list[str]:
        """Follow-on questions suggested by the Chatbot"""
        if self.simplify_response:
            return self.response["suggestions"]
        try:
            return [
                x["text"]
                for x in self.response["item"]["messages"][1]["suggestedResponses"]
            ]
        except KeyError:
            return None

    def __repr__(self) -> str:
        return f"<EdgeGPT.Query: {self.prompt}>"

    def __str__(self) -> str:
        return self.output if self.simplify_response else "\n\n".join(self.output)


class ImageQuery(Query):
    def __init__(self, prompt: str, **kwargs) -> None:
        kwargs["content_type"] = "image"
        super().__init__(prompt, **kwargs)

    def __repr__(self) -> str:
        return f"<EdgeGPT.ImageQuery: {self.prompt}>"


def test_cookie_rotation() -> None:
    for i in range(1, 50):
        q = Query(
            f"What is {i} in Roman numerals?  Give the answer in JSON",
            style="precise",
        )
        log(f"{i}: {Cookie.current_file_path.name}")
        log(q.code)
        log(f"Cookie count: {Cookie.request_count.get(Cookie.current_file_path.name)}")


def test_features() -> Query:
    try:
        q = Query(
            f"What is {i} in Roman numerals?  Give the answer in JSON", style="precise"
        )
        log(f"{i}: {Cookie.current_file_path.name}")
        print(f"{Cookie.current_file_index=}")
        print(f"{Cookie.current_file_path=}")
        print(f"{Cookie.current_data=}")
        print(f"{Cookie.dir_path=}")
        print(f"{Cookie.search_pattern=}")
        print(f"{Cookie.files()=}")
        print(f"{Cookie.image_token=}")
        print(f"{Cookie.import_next(discard=True)=}")
        print(f"{Cookie.rotate_cookies=}")
        print(f"{Cookie.files()=}")
        print(f"{Cookie.ignore_files=}")
        print(f"{Cookie.supplied_files=}")
        print(f"{Cookie.request_count=}")  # Keeps a tally of requests made in using each cookie file during this session
        print(f"{q=}")
        print(f"{q.prompt=}")
        print(f"{q.ignore_cookies=}")
        print(f"{q.style=}")
        print(f"{q.simplify_response=}")
        print(f"{q.locale=}")
        print(f"{q.output=}")
        print(q)
        print(f"{q.sources=}")
        print(f"{q.sources_dict=}")
        print(f"{q.suggestions=}")
        print(f"{q.code=}")  # All code as a single string
        print(f"{q.code_blocks=}")  # Individual code blocks
        print(f"{q.code_block_formats=}")  # The language/format of each code block (if given)
        print(f"{Query.index=}")  # Keeps an index of Query objects created
        print(f"{Query.image_dir_path=}")
    except Exception as E:
        raise Exception(E) from E
    finally:
        return q
