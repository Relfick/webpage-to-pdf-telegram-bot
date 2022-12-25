import telebot
import weasyprint
import validators
import time
from urllib.parse import urlparse


bot = telebot.TeleBot('HIDDEN_TOKEN')  # stored locally


def get_file_name(msg_text: str):
    o = urlparse(msg_text)
    file_name = o.netloc.replace('www.', '') + o.path
    if file_name[-1] == '/':
        file_name = file_name[:-1]
    file_name = file_name.replace('/', '_')
    file_name += '.pdf'
    return file_name


def prepare_response(msg: str, chat_id: int, verbose=True):
    if msg == '/start':
        return "Hello! Send link starting with http or https"
    elif validators.url(msg):
        if verbose:
            send_text(chat_id, "Wait...")
        try:
            f = weasyprint.HTML(msg).write_pdf()
        except weasyprint.urls.URLFetchingError:
            return "Can't open this link"
        return f
    else:
        return "Incorrect link!"


def send_response(chat_id, msg, file_name='result.pdf'):
    if type(msg) is str:
        send_text(chat_id, msg)
    else:
        send_document(chat_id, msg, file_name)


def send_text(chat_id: int, text: str):
    bot.send_message(chat_id, text)


def send_document(chat_id: int, f: bytes, file_name):
    bot.send_document(chat_id, f, visible_file_name=file_name)


@bot.message_handler(content_types=['text'])
def get_text_message(message: telebot.types.Message):
    msg_text = message.text
    chat_id = message.chat.id
    tic = time.perf_counter()

    response = prepare_response(msg_text, chat_id)

    if type(response) is bytes:
        file_name = get_file_name(msg_text)
        toc = time.perf_counter()
        total_time_str = f"Time: {toc - tic:0.4f} sec"
        send_response(chat_id, response, file_name)
        send_response(chat_id, total_time_str)
    else:
        send_response(chat_id, response)


bot.polling(none_stop=True, interval=0, skip_pending=True)
