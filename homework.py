from http import HTTPStatus
import logging
import os
import time

from dotenv import load_dotenv
import requests
import telebot

import exceptions


load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    encoding='utf-8',
    filemode='w'
)


def check_tokens():
    """Checks the availability of environment variables."""
    token_list = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    if not all(token_list):
        logging.critical('Not all tokens provided.')
        raise exceptions.NotAllTokensExist('One or more tokens are missing.')


def send_message(bot, message):
    """Sends message to Telegram chat."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug('Message was successfully sent.')
    except Exception as error:
        message = (f'An error occurred when sending message to the user:'
                   f' {error}')
        raise exceptions.TelegramSendError(message)


def get_api_answer(timestamp):
    """Returns the answer from API server."""
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
    except requests.RequestException as error:
        message = f'API request error: {error}'
        raise exceptions.APIResponseError(message)

    if response.status_code != HTTPStatus.OK:
        raise exceptions.HTTPStatusIsNotOK('Response status is not 200.')

    return response.json()


def check_response(response):
    """Checks params of the API response."""
    if not isinstance(response, dict):
        raise TypeError('Response is not an instance of the dict type.')

    if (homeworks := response.get('homeworks')) is None:
        raise KeyError('Response is missing valid key {homeworks}.')

    if not isinstance(response['homeworks'], list):
        raise TypeError('<homeworks> is not an instance of the list type.')


def parse_status(homework):
    """Returns the status of the homework."""
    if (homework_name := homework.get('homework_name')) is None:
        raise KeyError('Dict don`t have key {homework_name}')

    if not homework['status']:
        raise exceptions.HomeworkStatusIsNotDocumented(
            'This homework does not have any status.'
        )

    if homework['status'] not in HOMEWORK_VERDICTS:
        raise exceptions.HomeworkStatusIsNotDocumented(
            'The status of this homework is not documented.'
        )

    homework_name = homework['homework_name']
    verdict = HOMEWORK_VERDICTS[homework['status']]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Main function of the bot."""
    logging.debug('Bot is starting server poll...')
    check_tokens()
    bot = telebot.TeleBot(token=TELEGRAM_TOKEN)
    timestamp = 0
    status = 'send'
    while True:
        try:
            response = get_api_answer(timestamp)
            timestamp = response.get('current_date', timestamp)
            check_response(response)
            homeworks = response['homeworks']
            if not homeworks:
                logging.debug('No status changes.')
                continue
            last_homework = homeworks[0]
            if last_homework['status'] != status:
                message = parse_status(last_homework)
                if send_message(bot, message):
                    status = last_homework['status']
        except Exception as error:
            logging.error(f'Error while running the program: {error}.')
        finally:
            logging.debug(f'Waiting for {RETRY_PERIOD} seconds until the next '
                          f'server poll...')
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
