# Edge GPT
ChatGPT with internet access

<details>
<summary>

## Setup (optional)
Completely optional, but recommended if you have beta access to Bing Chat
</summary>

### Requirements (Optional)
- A Microsoft Account with early access to http://bing.com/chat
- Microsoft Edge

### Checking access (Optional)
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
  --stream
  --bing-cookie BING_COOKIE (Optional)
```

## Developer
Use Async for the best experience

```python
import asyncio
from EdgeGPT import Chatbot

def get_input(prompt):
    """
    Multi-line input function
    """
    # Display the prompt
    print(prompt, end="")

    # Initialize an empty list to store the input lines
    lines = []

    # Read lines of input until the user enters an empty line
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    # Join the lines, separated by newlines, and store the result
    user_input = "\n".join(lines)

    # Return the input
    return user_input


async def main():
    """
    Main function
    """
    print("Initializing...")
    bot = Chatbot()
    while True:
        prompt = get_input("\nYou:\n")
        if prompt == "!exit":
            break
        elif prompt == "!help":
            print(
                """
            !help - Show this help message
            !exit - Exit the program
            !reset - Reset the conversation
            """,
            )
            continue
        elif prompt == "!reset":
            await bot.reset()
            continue
        print("Bot:")
        print(
            (await bot.ask(prompt=prompt))["item"]["messages"][1]["adaptiveCards"][0][
                "body"
            ][0]["text"],
        )
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

```

## Work in progress
- Error handling

# Credits
- pig#8932 (Discord) - Sharing account with beta access
- [Jimmy-Z](https://github.com/Jimmy-Z) - Bugfixes
