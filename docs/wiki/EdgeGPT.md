<a id="EdgeGPT"></a>

# EdgeGPT

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
              options: dict = None,
              webpage_context: str | None = None,
              search_result: str = False) -> dict
```

Ask a question to the bot

<a id="EdgeGPT.Chatbot.ask_stream"></a>

#### ask\_stream

```python
async def ask_stream(prompt: str,
                     wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
                     conversation_style: CONVERSATION_STYLE_TYPE = None,
                     raw: bool = False,
                     options: dict = None,
                     webpage_context: str | None = None,
                     search_result: str = False) -> Generator[str, None, None]
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
