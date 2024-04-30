# Film Data Base Bot

This is a custom written training BOT based on the free API from
rapidapi: [OTT details](https://rapidapi.com/gox-ai-gox-ai-default/api/ott-details/)

## What does the project do

This bot supports the following commands:
* searches and provides information about the movie, the name of which will be transmitted to it
* searches and provides information about films that match the specified parameters
* searches and provides information about latest arrivals from different platforms

This functionality is implemented using a free API, the BOT also saves the search history of each user’s movies in 
the database and can return this history to users

## Why was writing the project useful?

Writing this BOT helped to understand the following:

* With the work of Python libraries for creating Telegram BOTs
* Interacting with third party APIs using the requests library
* Basic operations with databases using ORM PeeWee

## Instructions for Starting the Project

To start the BOT, follow next steps:

1. Install [Python version 3.12.2](https://www.python.org/downloads/release/python-3122/)


2. Clone the repository to your local machine:

```bash
git clone https://gitlab.skillbox.ru/tikhon_molochko/python_basic_diploma.git
```

3. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

4. Install the project dependencies:

```bash
pip install -r requirements.txt
```

5. Specify environment variables in the .env file

```bash
TELEBOT_TOKEN = YOUR_TELEBOT_TOKEN
RAPID_KEY = YOUR_RAPID_KEY
RAPID_HOST = YOUR_RAPID_HOST
```

6. Run the BOT:

```bash
python main.py
```

## BOT url: [Film Data Base](https://t.me/filmDataBaseBot)
