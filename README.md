<div align="center">
  <img src="https://socialify.git.ci/acheong08/EdgeGPT/image?font=Inter&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FHarry-Jing%2FEdgeGPT%2Fmaster%2F.readme%2FBing_favicon.png&owner=1&pattern=Floating%20Cogs&theme=Auto" alt="EdgeGPT" width="640" height="320" />

  # Edge GPT

  *The reverse engineering the chat feature of the new version of Bing*

</div>

<p align="center">
  <a href="https://github.com/acheong08/EdgeGPT">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/EdgeGPT">
  </a>
  <img alt="Python version" src="https://img.shields.io/badge/python-3.7+-blue.svg">
</p>

#  

> ## UPDATE 2023/02/11 - Public access has been revoked by Microsoft. It still works if you have access to the waitlist. Please check out https://github.com/acheong08/SydneyAuth if you do have access and contact me. You can securely share access with the community if you don't mind.

## Table of Contents
- [Steup](#steup)
- [Usage](#usage)
  - [Quick start](#quick-start)
  - [Developer demo](#developer-demo)
- [Work in progress](#work-in-progress)
- [Contributors](#contributors)

## Steup

### Install package
```bash
python3 -m pip install EdgeGPT
```
 
### Requirements 
 
- python 3.7+
- Microsoft Edge
- A Microsoft Account with early access to http://bing.com/chat


<details>
  <summary>
 
  ### Checking access
 
  </summary>
 
- Install the latest version of Microsoft Edge
- Open http://bing.com/chat
- If you see a chat feature, you are good to go
 
</details>


<details>
  <summary>
 
  ### Getting authentication
 
  </summary>

- Open the developer tools (F12)
- Go to the Application tab → Storage → Cookies
- Find the cookie named "_U"
- Copy the value of the cookie
 
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

usage: EdgeGPT.py [-h] [--no-stream] [--bing-cookie BING_COOKIE]

options:
  -h, --help            show this help message and exit
  --no-stream
  --bing-cookie BING_COOKIE (Required)
```

-----

### Developer demo
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


## Contributors
This project exists thanks to all the people who contribute. 
- pig#8932 (Discord) - Sharing account with beta access
- [Jimmy-Z](https://github.com/Jimmy-Z) - Bugfixes
 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>
