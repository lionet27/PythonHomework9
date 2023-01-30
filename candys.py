# 2) Создайте Бота для игры с конфетами человек против бота. (Дополнительно)


from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from random import randint as rd


bot = Bot(token='')
updater = Updater(token='')
dispatcher = updater.dispatcher

A = 0
B = 1


def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Давай сыграем! условия игры:Есть 120 конфет за раз можно взять не больше 28 конфет.Выигрывает тот, кто оставил на столе 0 конфет.Введи сколько конфет ты возьмешь.')
    return A

def firstMove(update, context):
    text = update.message.text
    tookCandys=int(text)
    candys=120
    
    if tookCandys<1 or tookCandys>28:
        context.bot.send_message(update.effective_chat.id, 'Вы ввели неправильное число конфет!Должно быть от 1 до 28!Введите еще раз сколько конфет вы возьмете:')
        return A
    else:
        candys=candys-tookCandys
        
        context.bot.send_message(update.effective_chat.id, f'Осталось {candys} конфет. ')
       
        # tookCandys=28
        tookCandys=rd(1,28)

        candys=candys-tookCandys
        context.bot.send_message(update.effective_chat.id, f'Я взял {tookCandys} конфет. Осталось {candys} конфет')
        context.bot.send_message(update.effective_chat.id, 'Введите сколько конфет вы возьмете на этот раз:')
        candys=str(candys)
        with open('candy.txt','w') as data:
            data.write(candys)
        return B

def mansMove(update, context):
    text = update.message.text
    tookCandys=int(text)
    with open('candy.txt','r') as data:
        candys=int(data.read())
                
    if candys<28:
        if tookCandys<1 or tookCandys>candys:
            context.bot.send_message(update.effective_chat.id, f'Вы взяли конфет больше,чем осталось! Вы можете взять от 1 до {candys}! Введите еще раз сколько конфет вы возьмете:')
            return B
    else:
        if tookCandys<1 or tookCandys>28:
            context.bot.send_message(update.effective_chat.id, 'Вы ввели неправильное число конфет!Должно быть от 1 до 28!Введите еще раз сколько конфет вы возьмете:')
            return B
    
    candys=candys-tookCandys
    
    if candys==0:
        context.bot.send_message(update.effective_chat.id, 'Поздравляю! Вы выиграли у меня!')
        context.bot.send_message(update.effective_chat.id, 'До свидания! Приходи еще поиграть!')
        return ConversationHandler.END
        # return fallbacks

    else:
        context.bot.send_message(update.effective_chat.id, f'Осталось {candys} конфет. ')
        if candys>56:
            tookCandys=rd(1,28)
        elif 29<candys<57:
            tookCandys=candys-29
        elif candys==29:
            tookCandys=1
        else:
            tookCandys=candys

        candys=candys-tookCandys
        context.bot.send_message(update.effective_chat.id, f'Я взял {tookCandys} конфет. Осталось {candys} конфет')
        
        if candys==0:
            context.bot.send_message(update.effective_chat.id, 'Поздравьте меня! Я выиграл!')
            context.bot.send_message(update.effective_chat.id, 'До свидания! С удовольствием сыграю с тобой еще раз!')
            return ConversationHandler.END

        else:
            candys=str(candys)
            with open('candy.txt','w') as data:
                data.write(candys)
            context.bot.send_message(update.effective_chat.id, 'Введите сколько конфет вы возьмете на этот раз:')
        return B


def cancel(update, context):
    context.bot.send_message(update.effective_chat.id, 'До свидания! С удовольствием сыграю с тобой еще раз!')
    return ConversationHandler.END

start_handler = CommandHandler('start', start)
firstMove_handler = MessageHandler(Filters.text, firstMove)
mansMove_handler = MessageHandler(Filters.text, mansMove)
cancel_handler = CommandHandler('cancel', cancel)

conv_handler = ConversationHandler(entry_points=[start_handler],
                                    states={A:[firstMove_handler],
                                    B:[mansMove_handler]},
                                    fallbacks=[cancel_handler])
dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()