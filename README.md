<div align="center">

# Edge GPT

*The reverse engineering the chat feature of the new version of Bing

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
- [Work in progress](#work-in-progress)
- [Contributing](#contributing)

## Steup

### Install package
```bash
python3 -m pip install EdgeGPT
```

<details>
<summary>
 
### Requirements (Required)
 
</summary>
 
- A Microsoft Account with early access to http://bing.com/chat
- Microsoft Edge
- python 3.7+
 
</details>


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

- Open the developer tools (F12)
- Go to the Application tab → Storage → Cookies
- Find the cookie named "_U"
- Copy the value of the cookie
 
</details>



## Usage

### Demo usage

 
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


## Contributors
This project exists thanks to all the people who contribute. 
- pig#8932 (Discord) - Sharing account with beta access
- [Jimmy-Z](https://github.com/Jimmy-Z) - Bugfixes
 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>
