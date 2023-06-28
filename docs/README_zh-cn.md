<div align="center">
  <img src="https://socialify.git.ci/acheong08/EdgeGPT/image?font=Inter&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F9%2F9c%2FBing_Fluent_Logo.svg&owner=1&pattern=Floating%20Cogs&theme=Auto" alt="EdgeGPT" width="640" height="320" />

# Edge GPT

_新必应聊天功能的逆向工程_

<a href="./README.md">English</a> -
<a>简体中文</a> -
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

# 设置

</summary>

## 安装模块

```bash
python3 -m pip install EdgeGPT --upgrade
```

## 要求


- python 3.8+
- 一个可以访问必应聊天的微软账户 <https://bing.com/chat> (可选，视所在地区而定)
- 需要在 New Bing 支持的国家或地区（中国大陆需使用VPN）
- [Selenium](https://pypi.org/project/selenium/) (对于需要自动配置cookie的情况)

## 身份验证

基本上不需要了。

**在部分地区**，微软已将聊天功能**开放**给所有人，或许可以**省略这一步**了。可以使用浏览器来确认（将 UA 设置为能表示为 Edge 的），**试一下能不能不登录就可以开始聊天**。

可能也得**看当前所在 IP 地址**。例如，如果试图从一个已知**属于数据中心范围**的 IP 来访问聊天功能（虚拟服务器、根服务器、虚拟专网、公共代理等），**可能就需要登录**；但是要是用家里的 IP 地址访问聊天功能，就没有问题。

如果收到这样的错误，可以试试**提供一个 cookie** 看看能不能解决：

`Exception: Authentication failed. You have not been accepted into the beta.`

### 收集 cookie

1. 获取一个看着像 Microsoft Edge 的浏览器。

 * a) (简单) 安装最新版本的 Microsoft Edge
 * b) (高级) 或者, 您可以使用任何浏览器并将用户代理设置为Edge的用户代理 (例如 `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`). 您可以使用像 "User-Agent Switcher and Manager"  [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg) 和 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/) 这样的扩展轻松完成此操作。

2. 打开 [bing.com/chat](https://bing.com/chat)
3. 如果您看到聊天功能，就接着下面的步骤...
4. 安装 [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 或 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) 的 cookie editor 扩展
5. 移步到 [bing.com](https://bing.com)
6. 打开扩展程序
7. 点击右下角的"导出" ，然后点击"导出为 JSON" (将会把内容保存到你的剪贴板上)
8. 把你剪贴板上的内容粘贴到 `bing_cookies_*.json` 文件中
   * 注意：**Cookie 文件名必须遵守正则表达式 `bing_cookies_*.json`**，这样才能让本模块的 cookie 处理程序识别到。



### 在代码中使用 cookie：
```python
cookies = json.loads(open("./path/to/cookies.json", encoding="utf-8").read()) # 可能会忽略 cookie 选项
bot = await Chatbot.create(cookies=cookies)
```

</details>

<details open>

<summary>

# 如何使用聊天机器人

</summary>

## 从命令行运行

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
（中/美/英/挪具有更好的本地化支持）

## 在 Python 运行

### 1. 使用 `Chatbot` 类和 `asyncio` 类以进行更精细的控制

使用 async 获得最佳体验，例如:

```python
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = await Chatbot.create() # 导入 cookie 是“可选”的，如前所述
    response = await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative, simplify_response=True)
    print(json.dumps(response, indent=2)) # 返回下面这些
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
---

## 使用 Docker 运行

假设当前工作目录有一个文件 `cookies.json`

```bash

docker run --rm -it -v $(pwd)/cookies.json:/cookies.json:ro -e COOKIE_FILE='/cookies.json' ghcr.io/acheong08/edgegpt
```

可以像这样添加任意参数

```bash

docker run --rm -it -v $(pwd)/cookies.json:/cookies.json:ro -e COOKIE_FILE='/cookies.json' ghcr.io/acheong08/edgegpt --rich --style creative
```

</details>

</details>

<details open>

<summary>

# 如何使用图片生成器

</summary>

## 从命令行运行

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

## 在 Python 运行

### 1)  `ImageQuery` 助手类

使用一个简易提示生成图像，并下载到当前工作目录：

```python
from EdgeGPT.EdgeUtils import ImageQuery

q=ImageQuery("Meerkats at a garden party in Devon")
```

在此会话中修改所有后续图像的下载目录：

```
Query.image_dirpath = Path("./to_another_folder")
```

### 2) 使用 `ImageGen` 类和 `asyncio` 类以进行更精细的控制

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
    parser.add_argument("-U", help="从浏览器获取的身份认证 cookie", type=str)
    parser.add_argument("--cookie-file", help="包含认证 cookie 的文件", type=str)
    parser.add_argument(
        "--prompt",
        help="用于生成图片的 prompt",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        help="输出目录",
        type=str,
        default="./output",
    )
    parser.add_argument(
        "--quiet", help="禁用管道消息", action="store_true"
    )
    parser.add_argument(
        "--asyncio", help="使用 asyncio 运行 ImageGen", action="store_true"
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
        raise Exception("未能找到认证 Cookie")

    if not args.asyncio:
        # 创建图像生成器
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

# Star 历史

</summary>

[![Star History Chart](https://api.star-history.com/svg?repos=acheong08/EdgeGPT&type=Date)](https://star-history.com/#acheong08/EdgeGPT&Date)

</details>

<details open>

<summary>

# 贡献者

</summary>

这个项目的存在要归功于所有做出贡献的人。

 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>

</details>
