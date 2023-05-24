<a id="EdgeGPT"></a>

# EdgeGPT

Main.py

<a id="EdgeGPT._ChatHubRequest"></a>

## \_ChatHubRequest Objects

```python
class _ChatHubRequest()
```

Request object for ChatHub

<a id="EdgeGPT._ChatHubRequest.update"></a>

#### update

```python
def update(prompt: str,
           conversation_style: CONVERSATION_STYLE_TYPE,
           options: list | None = None,
           webpage_context: str | None = None,
           search_result: bool = False) -> None
```

Updates request object

<a id="EdgeGPT._ChatHub"></a>

## \_ChatHub Objects

```python
class _ChatHub()
```

Chat API

<a id="EdgeGPT._ChatHub.ask_stream"></a>

#### ask\_stream

```python
async def ask_stream(
        prompt: str,
        wss_link: str,
        conversation_style: CONVERSATION_STYLE_TYPE = None,
        raw: bool = False,
        options: dict = None,
        webpage_context: str | None = None,
        search_result: bool = False) -> Generator[str, None, None]
```

Ask a question to the bot

<a id="EdgeGPT._ChatHub.close"></a>

#### close

```python
async def close() -> None
```

Close the connection

<a id="EdgeGPT.Chatbot"></a>

## Chatbot Objects

```python
class Chatbot()
```

Combines everything to make it seamless

```python
@staticmethod
async def create(
        proxy: str | None = None,
        cookies: list[dict] | None = None,
):
```
<a id="EdgeGPT.Chatbot.ask"></a>

#### ask

```python
async def ask(prompt: str,
              wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
              conversation_style: CONVERSATION_STYLE_TYPE = None,
              options: dict = None,
              webpage_context: str | None = None,
              search_result: bool = False) -> dict
```

Ask a question to the bot

<a id="EdgeGPT.Chatbot.ask_stream"></a>

#### ask\_stream

```python
async def ask_stream(
        prompt: str,
        wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
        conversation_style: CONVERSATION_STYLE_TYPE = None,
        raw: bool = False,
        options: dict = None,
        webpage_context: str | None = None,
        search_result: bool = False) -> Generator[str, None, None]
```

Ask a question to the bot

<a id="EdgeGPT.Chatbot.close"></a>

#### close

```python
async def close() -> None
```

Close the connection

<a id="EdgeGPT.Chatbot.reset"></a>

#### reset

```python
async def reset() -> None
```

Reset the conversation

<a id="EdgeGPT.async_main"></a>

#### async\_main

```python
async def async_main(args: argparse.Namespace) -> None
```

Main function

<a id="EdgeGPT.Cookie"></a>

## Cookie Objects

```python
class Cookie()
```

Convenience class for Bing Cookie files, data, and configuration. This Class
is updated dynamically by the Query class to allow cycling through >1
cookie/credentials file e.g. when daily request limits (current 200 per
account per day) are exceeded.

<a id="EdgeGPT.Cookie.files"></a>

#### files

```python
@classmethod
def files(cls)
```

Return a sorted list of all cookie files matching .search_pattern

<a id="EdgeGPT.Cookie.import_data"></a>

#### import\_data

```python
@classmethod
def import_data(cls)
```

Read the active cookie file and populate the following attributes:

  .current_filepath
  .current_data
  .image_token

<a id="EdgeGPT.Cookie.import_next"></a>

#### import\_next

```python
@classmethod
def import_next(cls)
```

Cycle through to the next cookies file.  Import it.  Mark the previous
file to be ignored for the remainder of the current session.

<a id="EdgeGPT.Query"></a>

## Query Objects

```python
class Query()
```

A convenience class that wraps around EdgeGPT.Chatbot to encapsulate input,
config, and output all together.  Relies on Cookie class for authentication

<a id="EdgeGPT.Query.__init__"></a>

#### \_\_init\_\_

```python
def __init__(prompt,
             style="precise",
             content_type="text",
             cookie_file=0,
             echo=True,
             echo_prompt=False)
```

**Arguments**:


- `prompt` - Text to enter into Bing Chat
- `style` - creative, balanced, or precise
- `content_type` - "text" for Bing Chat; "image" for Dall-e
- `cookie_file` - Path, filepath string, or index (int) to list of cookie paths
- `echo` - Print something to confirm request made
- `echo_prompt` - Print confirmation of the evaluated prompt

<a id="EdgeGPT.Query.send_to_bing"></a>

#### send\_to\_bing

```python
async def send_to_bing(echo=True, echo_prompt=False)
```

Creat, submit, then close a Chatbot instance.  Return the response

<a id="EdgeGPT.Query.output"></a>

#### output

```python
@property
def output()
```

The response from a completed Chatbot request

<a id="EdgeGPT.Query.sources"></a>

#### sources

```python
@property
def sources()
```

The source names and details parsed from a completed Chatbot request

<a id="EdgeGPT.Query.sources_dict"></a>

#### sources\_dict

```python
@property
def sources_dict()
```

The source names and details as a dictionary

<a id="EdgeGPT.Query.code"></a>

#### code

```python
@property
def code()
```

Extract and join any snippets of Python code in the response

<a id="EdgeGPT.Query.languages"></a>

#### languages

```python
@property
def languages()
```

Extract all programming languages given in code blocks

<a id="EdgeGPT.Query.suggestions"></a>

#### suggestions

```python
@property
def suggestions()
```

Follow-on questions suggested by the Chatbot
