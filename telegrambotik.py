import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json

TOKEN = "8165817286:AAG05D0uCQ4QeskaVcX6vffwbGjzKBhjEZU"
AUDD_API_KEY = "6b8c55e60195272ec4b66b4c5c28a9c3"

def start(update, context):
    update.message.reply_text("🎵 Отправь мне видео или аудио, и я найду песню!")

def handle_media(update, context):
    message = context.bot.send_message(
        chat_id=update.message.chat_id, text="⏳ Распознаю музыку..."
    )
    try:
        file = context.bot.get_file(update.message.video or update.message.audio or update.message.voice)
        file_url = file.file_path
        response = requests.post(
            "https://api.audd.io/",
            data={"api_token": AUDD_API_KEY, "url": file_url, "return": "apple_music,spotify"}
        )
        result = json.loads(response.text)
        if result["status"] == "success" and result["result"]:
            song = result["result"]
            reply = f"🎶 Песня: {song['title']}\n👤 Исполнитель: {song['artist']}\n💿 Альбом: {song['album']}\n"
            if "spotify" in song:
                reply += f"🎧 Spotify: {song['spotify']['external_urls']['spotify']}\n"
            if "apple_music" in song:
                reply += f"🍎 Apple Music: {song['apple_music']['url']}"
            context.bot.send_message(chat_id=update.message.chat_id, text=reply)
        else:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="❌ Не удалось распознать песню."
            )
    except Exception as e:
        context.bot.send_message(
            chat_id=update.message.chat_id, text=f"❌ Ошибка: {str(e)}"
        )
    context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video | Filters.audio | Filters.voice, handle_media))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
