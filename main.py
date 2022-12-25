import telebot
import weasyprint
import validators
import time
from urllib.parse import urlparse


def get_file_name(msg_text: str):
    o = urlparse(msg_text)
    file_name = o.netloc.replace('www.', '') + o.path
    if file_name[-1] == '/':
        file_name = file_name[:-1]
    file_name = file_name.replace('/', '_')
    file_name += '.pdf'
    return file_name


def prepare_response(msg: str):
    if msg == '/start':
        return "Hello! Send link starting with http or https"
    elif validators.url(msg):
        try:
            f = weasyprint.HTML(msg).write_pdf()
        except weasyprint.urls.URLFetchingError:
            return "Can't open this link"
        return f
    else:
        return "Incorrect link!"


def send_response(bot, chat_id, msg, file_name='result.pdf'):
    if type(msg) is str:
        bot.send_message(chat_id, msg)
    else:
        bot.send_document(chat_id, msg, visible_file_name=file_name)


if __name__ == '__main__':
    bot = telebot.TeleBot('HIDDEN_TOKEN')  # stored locally

    @bot.message_handler(content_types=['text'])
    def get_text_message(message: telebot.types.Message):
        msg_text = message.text
        chat_id = message.chat.id
        tic = time.perf_counter()

        response = prepare_response(msg_text)

        if type(response) is bytes:
            file_name = get_file_name(msg_text)
            toc = time.perf_counter()
            total_time_str = f"Time: {toc - tic:0.4f} sec"
            send_response(bot, chat_id, response, file_name)
            send_response(bot, chat_id, total_time_str)
        else:
            send_response(bot, chat_id, response)

    bot.polling(none_stop=True, interval=0, skip_pending=True)
