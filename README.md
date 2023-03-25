<div align="center">
  <img src="https://socialify.git.ci/acheong08/EdgeGPT/image?font=Inter&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F9%2F9c%2FBing_Fluent_Logo.svg&owner=1&pattern=Floating%20Cogs&theme=Auto" alt="EdgeGPT" width="640" height="320" />

# Edge GPT

_The reverse engineering the chat feature of the new version of Bing_

<a>English</a> -
<a href="./README_zh.md">中文</a>

</div>

<p align="center">
  <a href="https://github.com/acheong08/EdgeGPT">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/EdgeGPT">
  </a>
  <img alt="Python version" src="https://img.shields.io/badge/python-3.8+-blue.svg">
</p>

---

## Setup

### Install package

```bash
python3 -m pip install EdgeGPT --upgrade
```

### Requirements

- python 3.8+
- A Microsoft Account with early access to <https://bing.com/chat> (Required)
- Required in a supported country with New Bing (Chinese mainland VPN required)

<details>
  <summary>

### Checking access (Required)

  </summary>

- Install the latest version of Microsoft Edge
- Alternatively, you can use any browser and set the user-agent to look like you're using Edge (e.g., `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`). You can do this easily with an extension like "User-Agent Switcher and Manager" for [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg) and [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/).
- Open [bing.com/chat](https://bing.com/chat)
- If you see a chat feature, you are good to go

</details>

<details>
  <summary>

### Getting authentication (Required)

  </summary>

- Install the cookie editor extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to `bing.com`
- Open the extension
- Click "Export" on the bottom right (This saves your cookies to clipboard)
- Paste your cookies into a file `cookies.json`

</details>

<details>

<summary>

## Chatbot

</summary>

## Usage

### Quick start

```
 $ python3 -m EdgeGPT -h

        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit
        Enter twice to send message or set --enter-once to send one line message

usage: EdgeGPT.py [-h] [--enter-once] [--no-stream] [--rich] [--proxy PROXY] [--wss-link WSS_LINK] [--style {creative,balanced,precise}]
                  [--cookie-file COOKIE_FILE]

options:
  -h, --help            show this help message and exit
  --enter-once
  --no-stream
  --rich
  --proxy PROXY         Proxy URL (e.g. socks5://127.0.0.1:1080)
  --wss-link WSS_LINK   WSS URL(e.g. wss://sydney.bing.com/sydney/ChatHub)
  --style {creative,balanced,precise}
  --cookie-file COOKIE_FILE
                        needed if environment variable COOKIE_FILE is not set
```

---

### Developer demo

Three ways to pass in cookies:

- Environment variable: `export COOKIE_FILE=/path/to/cookies.json`.
- Specify the path to `cookies.json` in the argument `cookiePath` like this:

  ```python
  bot = Chatbot(cookiePath='./cookie.json')
  ```

- Pass in the cookies directly by the argument `cookies`, like this:

  ```python
  with open('./cookie.json', 'r') as f:
      cookies = json.load(f)
  bot = Chatbot(cookies=cookies)
  ```

Use Async for the best experience

Reference code for more advanced example of usage:

```python
import asyncio
from EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = Chatbot()
    print(await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub"))
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

```

</details>

<details>

<summary>

## Image generator

</summary>

```bash
$ python3 -m ImageGen -h
usage: ImageGen.py [-h] [-U U] [--cookie-file COOKIE_FILE] --prompt PROMPT [--output-dir OUTPUT_DIR]

options:
  -h, --help            show this help message and exit
  -U U                  Auth cookie from browser
  --cookie-file COOKIE_FILE
                        File containing auth cookie
  --prompt PROMPT       Prompt to generate images for
  --output-dir OUTPUT_DIR
                        Output directory
```

### Developer demo

```python
from ImageGen import ImageGen
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-U", help="Auth cookie from browser", type=str)
    parser.add_argument("--cookie-file", help="File containing auth cookie", type=str)
    parser.add_argument(
        "--prompt",
        help="Prompt to generate images for",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory",
        type=str,
        default="./output",
    )
    args = parser.parse_args()
    # Load auth cookie
    with open(args.cookie_file, encoding="utf-8") as file:
        cookie_json = json.load(file)
        for cookie in cookie_json:
            if cookie.get("name") == "_U":
                args.U = cookie.get("value")
                break

    if args.U is None:
        raise Exception("Could not find auth cookie")

    # Create image generator
    image_generator = ImageGen(args.U)
    image_generator.save_images(
        image_generator.get_images(args.prompt),
        output_dir=args.output_dir,
    )

```

</details>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=acheong08/EdgeGPT&type=Date)](https://star-history.com/#acheong08/EdgeGPT&Date)

## Contributors

This project exists thanks to all the people who contribute.

 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>
