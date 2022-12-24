import telebot
import weasyprint
import validators


bot = telebot.TeleBot('HIDDEN_TOKEN')  # stored locally


def prepare_response(msg: str, chat_id: int):
    if msg == '/start':
        return "Hello! Send link starting with http or https"
    elif validators.url(msg):
        send_text(chat_id, "Wait...")
        try:
            f = weasyprint.HTML(msg).write_pdf()
        except weasyprint.urls.URLFetchingError:
            return 0
        return f


def send_response(chat_id, msg):
    if type(msg) is str:
        send_text(chat_id, msg)
    else:
        send_document(chat_id, msg)


def send_text(chat_id: int, text: str):
    bot.send_message(chat_id, text)


def send_document(chat_id: int, f: bytes):
    bot.send_document(chat_id, f, visible_file_name='result.pdf')


@bot.message_handler(content_types=['text'])
def get_text_message(message: telebot.types.Message):
    msg_text = message.text
    chat_id = message.chat.id

    response = prepare_response(msg_text, chat_id)

    if response:
        send_response(chat_id, response)


bot.polling(none_stop=True, interval=0, skip_pending=True)
