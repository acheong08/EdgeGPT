<div align="center">
  <img src="https://socialify.git.ci/acheong08/EdgeGPT/image?font=Inter&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F9%2F9c%2FBing_Fluent_Logo.svg&owner=1&pattern=Floating%20Cogs&theme=Auto" alt="EdgeGPT" width="640" height="320" />

# Edge GPT

_The reverse engineering the chat feature of the new version of Bing_

<a>English</a> -
<a href="./README_zh-cn.md">简体中文</a> -
<a href="./README_zh-tw.md">繁體中文</a> -
<a href="./README_es.md">Español</a> -
<a href="./README_ja.md">日本語</a>

</div>

<p align="center">
  <a href="https://github.com/acheong08/EdgeGPT">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/EdgeGPT">
  </a>
  <img alt="Python version" src="https://img.shields.io/badge/python-3.8+-blue.svg">
  <img alt="Total downloads" src="https://static.pepy.tech/badge/edgegpt">

</p>

<details open>

<summary>

# Setup

</summary>

## Install package

```bash
python3 -m pip install EdgeGPT --upgrade
```

## Requirements

- python 3.8+
- A Microsoft Account with access to <https://bing.com/chat> (Optional, depending on your region)
- Required in a supported country or region with New Bing (Chinese mainland VPN required)
- [Selenium](https://pypi.org/project/selenium/) (for automatic cookie setup)

## Authentication

!!! POSSIBLY NOT REQUIRED ANYMORE !!!

**In some regions**, Microsoft has made the chat feature **available** to everyone, so you might be able to **skip this step**. You can check this with a browser (with user-agent set to reflect Edge), by **trying to start a chat without logging in**.

It was also found that it might **depend on your IP address**. For example, if you try to access the chat features from an IP that is known to **belong to a datacenter range** (vServers, root servers, VPN, common proxies, ...), **you might be required to log in** while being able to access the features just fine from your home IP address.

If you receive the following error, you can try **providing a cookie** and see if it works then:

`Exception: Authentication failed. You have not been accepted into the beta.`

### Collect cookies

1. Get a browser that looks like Microsoft Edge.

- a) (Easy) Install the latest version of Microsoft Edge
- b) (Advanced) Alternatively, you can use any browser and set the user-agent to look like you're using Edge (e.g., `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`). You can do this easily with an extension like "User-Agent Switcher and Manager" for [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg) and [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/).

2. Open [bing.com/chat](https://bing.com/chat)
3. If you see a chat feature, you are good to continue...
4. Install the cookie editor extension for [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
5. Go to [bing.com](https://bing.com)
6. Open the extension
7. Click "Export" on the bottom right, then "Export as JSON" (This saves your cookies to clipboard)
8. Paste your cookies into a file `bing_cookies_*.json`.
   - NOTE: The **cookies file name MUST follow the regex pattern `bing_cookies_*.json`**, so that they could be recognized by internal cookie processing mechanisms

### Use cookies in code:

```python
cookies = json.loads(open("./path/to/cookies.json", encoding="utf-8").read())  # might omit cookies option
bot = await Chatbot.create(cookies=cookies)
```

</details>

<details open>

<summary>

# How to use Chatbot

</summary>

## Run from Command Line

```
 $ python3 -m EdgeGPT.EdgeGPT -h

        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit

usage: EdgeGPT.py [-h] [--enter-once] [--search-result] [--no-stream] [--rich] [--proxy PROXY] [--wss-link WSS_LINK]
                  [--style {creative,balanced,precise}] [--prompt PROMPT] [--cookie-file COOKIE_FILE]
                  [--history-file HISTORY_FILE] [--locale LOCALE]

options:
  -h, --help            show this help message and exit
  --enter-once
  --search-result
  --no-stream
  --rich
  --proxy PROXY         Proxy URL (e.g. socks5://127.0.0.1:1080)
  --wss-link WSS_LINK   WSS URL(e.g. wss://sydney.bing.com/sydney/ChatHub)
  --style {creative,balanced,precise}
  --prompt PROMPT       prompt to start with
  --cookie-file COOKIE_FILE
                        path to cookie file
  --history-file HISTORY_FILE
                        path to history file
  --locale LOCALE       your locale (e.g. en-US, zh-CN, en-IE, en-GB)
```

(China/US/UK/Norway has enhanced support for locale)

## Run in Python

### 1. The `Chatbot` class and `asyncio` for more granular control

Use Async for the best experience, for example:

```python
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = await Chatbot.create() # Passing cookies is "optional", as explained above
    response = await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative, simplify_response=True)
    print(json.dumps(response, indent=2)) # Returns
    """
{
    "text": str,
    "author": str,
    "sources": list[dict],
    "sources_text": str,
    "suggestions": list[str],
    "messages_left": int
}
    """
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 2) The `Query` and `Cookie` helper classes 

Create a simple Bing Chat AI query (using the 'precise' conversation style by default) and see just the main text output rather than the whole API response:

Remeber to store your cookies in a specific format: `bing_cookies_*.json`.

```python
from EdgeGPT.EdgeUtils import Query, Cookie

q = Query("What are you? Give your answer as Python code")
print(q)
```

The default directory for storing Cookie files is `HOME/bing_cookies` but you can change it with:

```python
Cookie.dir_path = Path(r"...")
```

Or change the conversation style or cookie file to be used:

```python
q = Query(
  "What are you? Give your answer as Python code",
  style="creative",  # or: 'balanced', 'precise'
  cookie_file="./bing_cookies_alternative.json"
)

#  Use `help(Query)` to see other supported parameters.
```

Quickly extract the text output, code snippets, list of sources/references, or suggested follow-on questions from a response using the following attributes:

```python
q.output  # Also: print(q)
q.sources
q.sources_dict
q.suggestions
q.code
q.code_blocks
q.code_block_formatsgiven)
```

Get the orginal prompt and the conversation style you specified:

```python
q.prompt
q.ignore_cookies
q.style
q.simplify_response
q.locale
repr(q)
```

Access previous Queries made since importing `Query`:

```python
Query.index  # A list of Query objects; updated dynamically
Query.image_dir_path

```

And finally, the `Cookie` class supports multiple cookie files, so if you create additional cookie files with the naming convention `bing_cookies_*.json`, your queries will automatically try using the next file (alphabetically) if you've exceeded your daily quota of requests (currently set at 200).

Here are the main attributes which you can access:

```python
Cookie.current_file_index
Cookie.current_file_path
Cookie.current_data
Cookie.dir_path
Cookie.search_pattern
Cookie.files
Cookie.image_token
Cookie.import_next
Cookie.rotate_cookies
Cookie.ignore_files
Cookie.supplied_files
Cookie.request_count
```

---

## Run with Docker

This assumes you have a file cookies.json in your current working directory

```bash

docker run --rm -it -v $(pwd)/cookies.json:/cookies.json:ro -e COOKIE_FILE='/cookies.json' ghcr.io/acheong08/edgegpt
```

You can add any extra flags as following

```bash

docker run --rm -it -v $(pwd)/cookies.json:/cookies.json:ro -e COOKIE_FILE='/cookies.json' ghcr.io/acheong08/edgegpt --rich --style creative
```

</details>

</details>

<details open>

<summary>

# How to use Image generator

</summary>

## Run from Command Line

```bash
$ python3 -m ImageGen.ImageGen -h
usage: ImageGen.py [-h] [-U U] [--cookie-file COOKIE_FILE] --prompt PROMPT [--output-dir OUTPUT_DIR] [--quiet] [--asyncio]

optional arguments:
  -h, --help            show this help message and exit
  -U U                  Auth cookie from browser
  --cookie-file COOKIE_FILE
                        File containing auth cookie
  --prompt PROMPT       Prompt to generate images for
  --output-dir OUTPUT_DIR
                        Output directory
  --quiet               Disable pipeline messages
  --asyncio             Run ImageGen using asyncio
```

## Run in Python

### 1) The `ImageQuery` helper class

Generate images based on a simple prompt and download to the current working directory:

```python
from EdgeGPT.EdgeUtils import ImageQuery

q=ImageQuery("Meerkats at a garden party in Devon")
```

Change the download directory for all future images in this session:

```
Query.image_dirpath = Path("./to_another_folder")
```

### 2) The `ImageGen` class and `asyncio` for more granular control

```python
from EdgeGPT.ImageGen import ImageGen
import argparse
import json

async def async_image_gen(args) -> None:
    async with ImageGenAsync(args.U, args.quiet) as image_generator:
        images = await image_generator.get_images(args.prompt)
        await image_generator.save_images(images, output_dir=args.output_dir)

if __name__ == "__main__":
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
    parser.add_argument(
        "--quiet", help="Disable pipeline messages", action="store_true"
    )
    parser.add_argument(
        "--asyncio", help="Run ImageGen using asyncio", action="store_true"
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

    if not args.asyncio:
        # Create image generator
        image_generator = ImageGen(args.U, args.quiet)
        image_generator.save_images(
            image_generator.get_images(args.prompt),
            output_dir=args.output_dir,
        )
    else:
        asyncio.run(async_image_gen(args))

```

</details>

<details open>

<summary>

# Star History

</summary>

[![Star History Chart](https://api.star-history.com/svg?repos=acheong08/EdgeGPT&type=Date)](https://star-history.com/#acheong08/EdgeGPT&Date)

</details>

<details open>

<summary>

# Contributors

</summary>

This project exists thanks to all the people who contribute.

 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>

</details>
