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
async def start(event):  # Данная команда регистрирует нового пользователя,
    # либо отправляет окно состояния существующему
    global sheet
    for k in range(1, sheet.row_count + 1):
        row = sheet.row_values(k)
        if row[0] == event.chat.id:
            await me(event)
            return
    keyboard = [
        [Button.text("a", resize=True), Button.text("b", resize=True)]
    ]
    last_id = len(sheet.col_values(1)) + 1

    # array = [telegram_id, username, state, exp, level, stamina, max_stamina, time_to_regen, player_class, money]
    # cell_list = sheet.range("A{0}:G{1}".format(last_id, last_id))
    # for i, val in enumerate(array):
    #    cell_list[i].value = val
    # sheet.update_cells(cell_list)
    await event.respond("Добро пожаловать в Текстовая игра жанра RPG.", buttons=keyboard)


@bot.on(events.NewMessage(pattern=r'^/me$'))
async def me(event):  # Данная команда отправляет окно состояния пользователю
    pass


@bot.on(events.NewMessage(pattern=r'^/help'))
async def help_wiki(event):  # Данная команда показывает пользователю функционал бота на данный момент
    await event.respond('''Данный бот имеет две кнопки:
- a, которая пишет a
- b, которая пишет b''')


bot.run_until_disconnected()
