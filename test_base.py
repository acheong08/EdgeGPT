import pytest
import asyncio
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

def test_base():
    asyncio.run(test_ask())

async def test_ask():
    bot = await Chatbot.create() # Passing cookies is "optional", as explained above
    response = await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative)
    await bot.close()
    assert response != ""
