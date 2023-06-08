import pytest
import asyncio
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = await Chatbot.create() # Passing cookies is "optional", as explained above
    response = await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative)
    await bot.close()
    assert response != ""

def test_base():
    assert 1+1==2
