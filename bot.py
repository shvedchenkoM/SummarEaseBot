import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from summarizer import Summarizer
import logging

load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm your summarization bot. Here's what I can do:\n"
        "1️⃣ Collect group messages.\n"
        "2️⃣ Summarize conversations.\n"
        "3️⃣ Show all collected messages.\n"
        "\nTry these commands:\n"
        "/start - Show this message\n"
        "/summarize - Summarize group messages\n"
        "/show_messages - Display all stored messages\n"
        "/reset_messages - Clear all stored messages"
    )


class SummarizationBot:
    def __init__(self):
        self.messages = []
        self.summarizer = Summarizer()

    async def collect_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message and update.message.text:
            author = update.message.from_user.first_name
            text = update.message.text
            self.messages.append({"author": author, "text": text})

    async def show_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.messages:
            await update.message.reply_text("❌ No messages stored yet!")
        else:
            all_messages = "\n".join([f"{msg['author']}: {msg['text']}" for msg in self.messages])
            await update.message.reply_text(f"📜 All collected messages:\n{all_messages}")

    async def summarize(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            if not self.messages:
                await update.message.reply_text("❌ No messages to summarize yet! Send some messages first.")
                return
            summary = self.summarizer.generate_summary(self.messages)
            await update.message.reply_text(f"📄 Summary:\n{summary}")
            self.messages = []
        except Exception as e:
            logger.error(f"Error in summarizing messages: {e}")
            await update.message.reply_text("❌ An error occurred while summarizing messages.")

    async def reset_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.messages = []
        await update.message.reply_text("✅ Messages have been reset.")

def main():
    bot = SummarizationBot()
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.collect_messages))
    application.add_handler(CommandHandler("show_messages", bot.show_messages))
    application.add_handler(CommandHandler("summarize", bot.summarize))
    application.add_handler(CommandHandler("reset_messages", bot.reset_messages))

    logger.info("🤖 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
