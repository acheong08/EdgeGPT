import json
from EdgeGPT import Chatbot


async def main():
    bot = Chatbot()
    await bot.start()

    result = json.dumps(
        await bot.ask("Check GitHub for a repository names 'EdgeGPT'"), indent=4
    )
    print(result)

    await bot.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
