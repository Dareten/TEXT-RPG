import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telethon import TelegramClient, events, Button

import config

scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('SIPI.json', scope)
google_client = gspread.authorize(creds)
sheet = google_client.open('SIPI').worksheet('MAIN')
bot = TelegramClient('SIPI', config.api_code, config.api_hash,
                     auto_reconnect=True).start(bot_token=config.token)


@bot.on(events.NewMessage(pattern=r'^/start$'))
async def start(event):
    if event.text != "/start":
        await event.reply("Используйте команду /start")
    else:
        keyboard = [
            [Button.text("a")],
            [Button.text("b")]
        ]
        await event.respond("Добро пожаловать в Текстовая игра жанра RPG.", buttons=keyboard)


@bot.on(events.NewMessage(pattern=r'^/help'))
async def help_wiki(event):
    await event.respond('''Данный бот имеет две кнопки:
- a, которая пишет a
- b, которая пишет b''')

bot.run_until_disconnected()
