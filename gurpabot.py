#ramazan telegram bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


BTN_TODAY,BTN_TOMORROW,BTN_CALENDAR,BTN_REGION,BTN_DUO = ('⏳ Bugun','⏳ Ertaga', '📆 To`liq taqvim', '🇺🇿 Mintaqa', '🤲 Duo')

main_buttons = ReplyKeyboardMarkup([
    [BTN_TODAY], [BTN_TOMORROW], [BTN_CALENDAR], [BTN_REGION], [BTN_DUO]
], resize_keyboard=True)

STATE_REGION = 1
STATE_CALENDAR = 2

def start(update, context):
    user = update.message.from_user
    buttons = [
        [
            InlineKeyboardButton('Toshkent', callback_data='min_1'),
            InlineKeyboardButton('Andijon', callback_data='min_2')
        ]
    ]
    update.message.reply_html('Assalomu alaykum <b>{}!</b>>'.
        format(user.first_name), reply_markup=InlineKeyboardMarkup(buttons))
    return STATE_REGION

def inline_callback(update, context):
    try:
        query = update.callback_query
        query.message.delete()
        query.message.reply_html(text='<b>Ramazon taqvimi</b> 2️⃣0️⃣2️⃣0️⃣\n \nQuyidagilardan birini tanlang👇', reply_markup=main_buttons)
        
        return STATE_CALENDAR
    except Exception as e:
        print('error', str(e))

def calendar_today(update, context):
    update.massage.reply_text('Bugun belgilandi')
def calendar_tomorrow(update, context):
    update.massage.reply_text('Ertaga belgilandi')
def calendar_month(update, context):
    update.massage.reply_text('To`liq taqvim belgilandi')
def select_region(update, context):
    update.massage.reply_text('Mintaqz tanlash')
def select_duo(update, context):
    update.massage.reply_text('Duo ko`rish belgilandi')

def main():
    updater = Updater('1231949765:AAGHWZ59obdFmfLtp2HoyP5zrKEa691Llxo', use_context = True)
    dispatcher = updater.dispatcher
    #dispatcher.add_handler(CommandHandler('start', start))
    #dispatcher.add_handler(CallbackQueryHandler(inline_callback))
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states={
            STATE_REGION: [CallbackQueryHandler(inline_callback)],
            STATE_CALENDAR: [
                MessageHandler(Filters.regex('^('+BTN_TODAY+')$'), calendar_today),
                MessageHandler(Filters.regex('^('+BTN_TOMORROW+')$'), calendar_tomorrow),
                MessageHandler(Filters.regex('^('+BTN_CALENDAR+')$'), calendar_month),
                MessageHandler(Filters.regex('^('+BTN_REGION+')$'), select_region),
                MessageHandler(Filters.regex('^('+BTN_DUO+')$'), select_duo)
            ],
        }, 
        fallbacks=[CommandHandler('start', start)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
main()
