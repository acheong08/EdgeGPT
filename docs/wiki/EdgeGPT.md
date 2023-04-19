<a id="EdgeGPT"></a>

# EdgeGPT

Main.py

<a id="EdgeGPT.__ChatHubRequest"></a>

## \_\_ChatHubRequest Objects

```python
class __ChatHubRequest()
```

Request object for ChatHub

<a id="EdgeGPT.__ChatHubRequest.update"></a>

#### update

```python
def update(prompt: str,
           conversation_style: CONVERSATION_STYLE_TYPE,
           options: list | None = None) -> None
```

Updates request object

<a id="EdgeGPT.__ChatHub"></a>

## \_\_ChatHub Objects

```python
class __ChatHub()
```

Chat API

<a id="EdgeGPT.__ChatHub.ask_stream"></a>

#### ask\_stream

```python
async def ask_stream(prompt: str,
                     wss_link: str,
                     conversation_style: CONVERSATION_STYLE_TYPE = None,
                     raw: bool = False,
                     options: dict = None) -> Generator[str, None, None]
```

Ask a question to the bot

<a id="EdgeGPT.__ChatHub.close"></a>

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

<a id="EdgeGPT.Chatbot.ask"></a>

#### ask

```python
async def ask(prompt: str,
              wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
              conversation_style: CONVERSATION_STYLE_TYPE = None,
              options: dict = None) -> dict
```

Ask a question to the bot

<a id="EdgeGPT.Chatbot.ask_stream"></a>

#### ask\_stream

```python
async def ask_stream(prompt: str,
                     wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
                     conversation_style: CONVERSATION_STYLE_TYPE = None,
                     raw: bool = False,
                     options: dict = None) -> Generator[str, None, None]
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

<a id="EdgeGPT.get_input_async"></a>

#### get\_input\_async

```python
async def get_input_async(session: PromptSession = None,
                          completer: WordCompleter = None) -> str
```

Multiline input function.

<a id="EdgeGPT.async_main"></a>

#### async\_main

```python
async def async_main(args: argparse.Namespace) -> None
```

Main function
