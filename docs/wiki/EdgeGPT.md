<a id="EdgeGPT"></a>

# EdgeGPT

Main.py

<a id="EdgeGPT.append_identifier"></a>

#### append\_identifier

```python
def append_identifier(msg: dict) -> str
```

Appends special character to end of message to identify end of message

<a id="EdgeGPT.get_ran_hex"></a>

#### get\_ran\_hex

```python
def get_ran_hex(length: int = 32) -> str
```

Returns random hex string

<a id="EdgeGPT.ChatHubRequest"></a>

## ChatHubRequest Objects

```python
class ChatHubRequest()
```

Request object for ChatHub

<a id="EdgeGPT.ChatHubRequest.update"></a>

#### update

```python
def update(prompt: str,
           conversation_style: CONVERSATION_STYLE_TYPE,
           options: list | None = None) -> None
```

Updates request object

<a id="EdgeGPT.Conversation"></a>

## Conversation Objects

```python
class Conversation()
```

Conversation API

<a id="EdgeGPT.ChatHub"></a>

## ChatHub Objects

```python
class ChatHub()
```

Chat API

<a id="EdgeGPT.ChatHub.ask_stream"></a>

#### ask\_stream

```python
async def ask_stream(
    prompt: str,
    wss_link: str,
    conversation_style: CONVERSATION_STYLE_TYPE = None
) -> Generator[str, None, None]
```

Ask a question to the bot

<a id="EdgeGPT.ChatHub.close"></a>

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
              conversation_style: CONVERSATION_STYLE_TYPE = None) -> dict
```

Ask a question to the bot

<a id="EdgeGPT.Chatbot.ask_stream"></a>

#### ask\_stream

```python
async def ask_stream(
    prompt: str,
    wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
    conversation_style: CONVERSATION_STYLE_TYPE = None
) -> Generator[str, None, None]
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
