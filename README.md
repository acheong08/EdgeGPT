<div align="center">
  <img src="https://socialify.git.ci/acheong08/EdgeGPT/image?font=Inter&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F9%2F9c%2FBing_Fluent_Logo.svg&owner=1&pattern=Floating%20Cogs&theme=Auto" alt="EdgeGPT" width="640" height="320" />

  # Edge GPT

  *The reverse engineering the chat feature of the new version of Bing*

</div>

<p align="center">
  <a href="https://github.com/acheong08/EdgeGPT">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/EdgeGPT">
  </a>
  <img alt="Python version" src="https://img.shields.io/badge/python-3.8+-blue.svg">
</p>

---

## Table of Contents
- [Edge GPT](#edge-gpt)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Install package](#install-package)
    - [Requirements](#requirements)
    - [Checking access (Required)](#checking-access-required)
    - [Getting authentication (Required)](#getting-authentication-required)
  - [Usage](#usage)
    - [Quick start](#quick-start)
    - [Developer demo](#developer-demo)
  - [Work in progress](#work-in-progress)
  - [Star History](#star-history)
  - [Contributors](#contributors)

## Setup

### Install package
```bash
python3 -m pip install EdgeGPT --upgrade
```

### Requirements
- python 3.8+
- A Microsoft Account with early access to http://bing.com/chat (Required)


<details>
  <summary>

  ### Checking access (Required)

  </summary>

- Install the latest version of Microsoft Edge
- Open http://bing.com/chat
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



## Usage

### Quick start

```
 $ python3 -m EdgeGPT -h

        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit
        Enter twice to send message

usage: EdgeGPT.py [-h] [--no-stream] --cookie-file COOKIE_FILE

options:
  -h, --help            show this help message and exit
  --no-stream
  --cookie-file COOKIE_FILE
```

-----

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

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=acheong08/EdgeGPT&type=Date)](https://star-history.com/#acheong08/EdgeGPT&Date)


## Contributors
This project exists thanks to all the people who contribute.

 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>
