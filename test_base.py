import pytest
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_ask():
    bot = await Chatbot.create()  # Passing cookies is "optional", as explained above
    response = await bot.ask(
        prompt="Hello world", conversation_style=ConversationStyle.creative
    )
    await bot.close()
    print(response)
    assert response != ""
