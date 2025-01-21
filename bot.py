from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from summarizer import summarize_messages  # Import the summarize function
import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("BOT_TOKEN")
messages = []
print(TELEGRAM_API_TOKEN)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm your summarization bot. Here's what I can do:\n"
        "1️⃣ Collect group messages.\n"
        "2️⃣ Summarize conversations.\n"
        "3️⃣ Show all collected messages.\n"
        "\nTry these commands:\n"
        "/start - Show this message\n"
        "/summarize - Summarize group messages\n"
        "/show_messages - Display all stored messages"
    )

# /summarize command
async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messages
    if not messages:
        await update.message.reply_text("❌ No messages to summarize yet! Send some messages first.")
        return

    summary = summarize_messages(messages)
    await update.message.reply_text(f"📄 Summary:\n{summary}")
    messages = []

# /show_messages command
async def show_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messages
    if not messages:
        await update.message.reply_text("❌ No messages stored yet!")
    else:
        all_messages = "\n".join(messages)
        await update.message.reply_text(f"📜 All collected messages:\n{all_messages}")


async def collect_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messages
    if update.message and update.message.text:
        messages.append(update.message.text)
        # await update.message.reply_text("✅ Message stored!")


# Main function to set up the bot
def main():
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_messages))
    application.add_handler(CommandHandler("show_messages", show_messages))
    application.add_handler(CommandHandler("summarize", summarize))

    print("🤖 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
