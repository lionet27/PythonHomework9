# Напишите Бота, удаляющего из текста все слова, содержащие "абв". (Ввод от пользователя)
# Пример: привет приабвет ограбпв
# Ответ: привет ограбпв

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


bot = Bot(token='')
updater = Updater(token='')
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Hello')


def voice(update, context):
    text = update.message.text
    
    text1=text.split()
    textWithoutDel=[]
    delText="абв"
    for el in text1:
        if delText not in el:
            textWithoutDel.append(el)
    newtext=' '.join(textWithoutDel)
    
    context.bot.send_message(update.effective_chat.id, newtext)
    


start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text, voice)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle() 