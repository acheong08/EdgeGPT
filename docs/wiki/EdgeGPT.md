<a id="EdgeGPT.EdgeGPT"></a>

# EdgeGPT.EdgeGPT

Main.py

<a id="EdgeGPT.EdgeGPT.Chatbot"></a>

## Chatbot Objects

```python
class Chatbot()
```

Combines everything to make it seamless

<a id="EdgeGPT.EdgeGPT.Chatbot.save_conversation"></a>

#### save\_conversation

```python
async def save_conversation(filename: str) -> None
```

Save the conversation to a file

<a id="EdgeGPT.EdgeGPT.Chatbot.load_conversation"></a>

#### load\_conversation

```python
async def load_conversation(filename: str) -> None
```

Load the conversation from a file

<a id="EdgeGPT.EdgeGPT.Chatbot.get_conversation"></a>

#### get\_conversation

```python
async def get_conversation() -> dict
```

Gets the conversation history from conversation_id (requires load_conversation)

<a id="EdgeGPT.EdgeGPT.Chatbot.get_activity"></a>

#### get\_activity

```python
async def get_activity() -> dict
```

Gets the recent activity (requires cookies)

<a id="EdgeGPT.EdgeGPT.Chatbot.ask"></a>

#### ask

```python
async def ask(prompt: str,
              wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
              conversation_style: CONVERSATION_STYLE_TYPE = None,
              webpage_context: str | None = None,
              search_result: bool = False,
              locale: str = guess_locale(),
              simplify_response: bool = False) -> dict
```

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

<a id="EdgeGPT.EdgeGPT.Chatbot.ask_stream"></a>

#### ask\_stream

```python
async def ask_stream(
    prompt: str,
    wss_link: str = "wss://sydney.bing.com/sydney/ChatHub",
    conversation_style: CONVERSATION_STYLE_TYPE = None,
    raw: bool = False,
    webpage_context: str | None = None,
    search_result: bool = False,
    locale: str = guess_locale()
) -> Generator[bool, dict | str, None]
```

Ask a question to the bot

<a id="EdgeGPT.EdgeGPT.Chatbot.close"></a>

#### close

```python
async def close() -> None
```

Close the connection

<a id="EdgeGPT.EdgeGPT.Chatbot.delete_conversation"></a>

#### delete\_conversation

```python
async def delete_conversation(conversation_id: str = None,
                              conversation_signature: str = None,
                              client_id: str = None) -> None
```

Delete the chat in the server and close the connection

<a id="EdgeGPT.EdgeGPT.Chatbot.reset"></a>

#### reset

```python
async def reset(delete=False) -> None
```

Reset the conversation
