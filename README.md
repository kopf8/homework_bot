# homework_bot
### homework_bot is a Telegram bot that accesses the Yandex.Practicum API server and gets the status of your homework.

## Project description

* Polls Yandex.Practicum API server every 10 minutes and checks the status of the homework sent for review.
* When the status is updated, bot analyzes the API response and sends you a corresponding notification in Telegram chat.
* Logs its work and informs you about important problems via Telegram chat.
* Each message in log consists of date and time of the event, the level of importance of the event, and a description of the event.

### Project tech stack:

Python, Telegram BOT API, Yandex.Practicum API

### How to run the project:

Clone repository and switch to project directory using command line:

```
git@github.com:kopf8/homework_bot.git
```

```
cd homework_bot
```

Create & activate virtual environment:

```
python -m venv .venv
```

* For Linux/macOS:

    ```
    source .venv/bin/activate
    ```

* For Win:

    ```
    source .venv/Scripts/activate
    ```

Upgrade pip:

```
python -m pip install --upgrade pip
```

Create .env file and fill it as per example:

```
PRACTICUM_TOKEN=<Your token received from Yandex Practicum API>_
TELEGRAM_TOKEN=<Your Telegram API token>
TELEGRAM_CHAT_ID=<Your Telegram chat ID>
```

Install project requirements from file _requirements.txt_:

```
pip install -r requirements.txt
```

### Author:
**Maria Kirsanova**<br>
Github profile — https://github.com/kopf8