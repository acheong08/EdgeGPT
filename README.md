# Edge GPT
ChatGPT with internet access

> ## UPDATE 2023/02/11 - Microsoft has suspended our shared account. If you have access to the new Bing, I have written a tool to securly share access (and also a token system which you can possible charge people for access to your API). Contact me at acheong@student.dalat.org if you're interested. The API system is open source: https://github.com/acheong08/SydneyAuth
> ### If you're alturistic and a fan of open source, please host it for free.

<details>
<summary>

## Setup (Required)
</summary>

### Requirements (Required)
- A Microsoft Account with early access to http://bing.com/chat
- Microsoft Edge

### Checking access (Required)
- Install the latest version of Microsoft Edge
- Open http://bing.com/chat
- If you see a chat feature, you are good to go

### Getting authentication (Optional)
- Open the developer tools (F12)
- Go to the Application tab → Storage → Cookies
- Find the cookie named "_U"
- Copy the value of the cookie

</details>

## Installation
- `python3 -m pip install EdgeGPT`

## Demo usage
```
 $ python3 -m EdgeGPT -h

        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit
        Enter twice to send message

usage: EdgeGPT.py [-h] [--stream] [--bing-cookie BING_COOKIE]

options:
  -h, --help            show this help message and exit
  --no-stream
  --bing-cookie BING_COOKIE (Required)
```

## Developer
Use Async for the best experience

[Reference code](https://github.com/acheong08/EdgeGPT/blob/master/src/EdgeGPT.py#L268-L328) for more advanced example of usage

```python
import asyncio
from EdgeGPT import Chatbot

async def main():
    bot = Chatbot()
    print(await bot.ask(prompt="Hello world"))
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

```

## Work in progress
- Error handling

# Credits
- pig#8932 (Discord) - Sharing account with beta access
- [Jimmy-Z](https://github.com/Jimmy-Z) - Bugfixes
