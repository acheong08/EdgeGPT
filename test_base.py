import pytest
from EdgeGPT.EdgeGPT import Chatbot
from EdgeGPT.EdgeGPT import ConversationStyle

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_ask():
    bot = await Chatbot.create()  # Passing cookies is "optional", as explained above
    response = await bot.ask(
        prompt="Hello world",
        conversation_style=ConversationStyle.creative,
    )
    response: str = response["item"]["messages"][1]["adaptiveCards"][0]["body"][0][
        "text"
    ]
    await bot.close()
    print(response)
    assert response != ""
