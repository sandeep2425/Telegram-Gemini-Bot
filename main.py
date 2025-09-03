import os
import asyncio
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# -------------------------------
# Configure Gemini
# -------------------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# start chat session with memory
chat_session = model.start_chat(history=[])

# -------------------------------
# Configure logging
# -------------------------------
logging.basicConfig(level=logging.INFO)

# -------------------------------
# Initialize bot and dispatcher
# -------------------------------
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher()

# -------------------------------
# Helpers
# -------------------------------
def clear_context():
    global chat_session
    chat_session = model.start_chat(history=[])  # reset conversation


# -------------------------------
# Handlers
# -------------------------------
@dispatcher.message(Command("start"))
async def command_start_handler(message: Message):
    await message.reply("Welcome! I'm your Gemini-powered bot 🚀")

@dispatcher.message(Command("help"))
async def command_help_handler(message: Message):
    help_command = """
/start - Start the bot
/clear - Clear the past conversation and reset context
/help - Show this help message
"""
    await message.reply(help_command)

@dispatcher.message(Command("clear"))
async def command_clear_handler(message: Message):
    clear_context()
    await message.reply("✅ Past conversation is cleared.")

@dispatcher.message()
async def gemini_handler(message: Message):
    """
    Handle normal text messages with Gemini (with memory).
    """
    print(f">>> USER: \n\t{message.text}")

    # Send message to Gemini chat session
    response = chat_session.send_message(message.text)

    # Log and reply back
    print(f">>> Gemini: \n\t{response.text}")
    await message.answer(response.text)


# -------------------------------
# Main
# -------------------------------
async def main():
    await dispatcher.start_polling(bot, skip_updates=False)

if __name__ == "__main__":
    asyncio.run(main())
