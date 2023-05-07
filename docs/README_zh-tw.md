<div align="center">
  <img src="https://socialify.git.ci/acheong08/EdgeGPT/image?font=Inter&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F9%2F9c%2FBing_Fluent_Logo.svg&owner=1&pattern=Floating%20Cogs&theme=Auto" alt="EdgeGPT" width="640" height="320" />

# Edge GPT

_新必應的逆向工程_

<a href="./README.md">English</a> -
<a href="./README_zh-cn.md">简体中文</a> -
<a>繁體中文 (中國臺灣)</a> -
<a href="./README_es.md">Español</a> -
<a href="./README_ja.md">日本語</a>

</div>

<p align="center">
  <a href="https://github.com/acheong08/EdgeGPT">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/EdgeGPT">
  </a>
  <img alt="Python version" src="https://img.shields.io/badge/python-3.8+-blue.svg">
</p>

---

## 設置

### 安裝模組

```bash
python3 -m pip install EdgeGPT --upgrade
```

### 要求

- python 3.8+
- 一個已經通過候補名單的微軟賬戶 <https://bing.com/chat> (必填)
- 需要在 New Bing 支持的國家 (中國大陸需使用VPN)

<details>
  <summary>

### 檢查訪問權限 (必需)

  </summary>

- 安裝最新版本的 Microsoft Edge
- 或者, 您可以使用任何瀏覽器並將用戶代理設置為Edge的用戶代理 (例如`Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`). 您可以使用像 "User-Agent Switcher and Manager" [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg) 和 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/) 這樣的擴展輕鬆完成此操作.
- 打開 [bing.com/chat](https://bing.com/chat)
- 如果您看到聊天功能，就準備就緒

</details>

<details>
  <summary>

### 獲取身份驗證 (必需)

  </summary>

- 安裝 [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 或 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) 的 cookie editor 擴展
- 轉到 `bing.com`
- 打開擴展程式
- 點擊右下角的"匯出" (將會把內容保存到你的剪貼簿上)
- 把你剪貼簿上的內容粘貼到 `cookies.json` 文件中

</details>

<details>

<summary>

## Chatbot

</summary>

## 使用方法

### 快速開始

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

### 開發演示

傳入 cookie 的三種方式:

- 設置環境變數: `export COOKIE_FILE=/path/to/cookies.json`.
- 像這樣把 `cookies.json`  的路徑傳入`cookie_path` 參數中:

  ```python
  bot = Chatbot(cookie_path='./cookies.json')
  ```

- 通過參數 `cookie` 傳入 cookie，如下所示:

  ```python
  with open('./cookies.json', 'r') as f:
      cookies = json.load(f)
  bot = Chatbot(cookies=cookies)
  ```

使用 aysnc 獲得最佳體驗

更高級用法範例的參考代碼：

```python
import asyncio
from EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = Chatbot()
    print(await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative,wss_link="wss://sydney.bing.com/sydney/ChatHub"))
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

```

</details>

<details>

<summary>

## 圖片生成

</summary>

```bash
$ python3 -m ImageGen -h
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

### 開發演示

```python
from ImageGen import ImageGen
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

## Star歷史

[![Star歷史](https://api.star-history.com/svg?repos=acheong08/EdgeGPT&type=Date)](https://star-history.com/#acheong08/EdgeGPT&Date)

## 貢獻者

這個項目的存在要歸功於所有做出貢獻的人。

 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>
