<div align="center">

# Telegram Bot for export chats (Linux)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
</div>

# Table of contents  
1. [Tech Stack](#Stack) 
2. [Features](#Features)
3. [Config](#Config)
4. [Run Locally](#run)
5. [Feedback](#Feedback)
6. [License](#License)
<div id="Stack">

## Tech Stack  

**Client:** Telegram 

**Server:** Python, Linux, python-telegram-bot
</div>
<div id="Features">

## Features  

- Export chats from account
- Send files for user
</div>
<div id="Config">

## Config

...is read from `config.py`

Format:
```python
TOKEN = r"1234567890:ABCDEFGHIJKLMmopQrSTuV1234567891jM"

APP_ID = r"12345678"

APP_HASH = r"f2c3bbd38a2a6fb7788c8e12f9b382a"
```
* `TOKEN` must be obtained from Telegram. [Bot Father](https://telegram.me/BotFather);

* `APP_ID` and `APP_HASH` must be obtained from Telegram. [Telegram App](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id;)
</div>
<div id="run">

## Run Locally  

Clone the project  

~~~bash  
  git clone https://github.com/ka9mal6t/tg_bot_for_export_chats.git
~~~

Go to the project directory  

~~~bash  
  cd tg_bot_for_export_chats
~~~

Install dependencies  

~~~bash  
pip install -r requirements.txt
~~~

Start the server  

~~~bash  
python main.py
~~~

</div>
<div id="Feedback">

## Feedback

If you have any feedback, please reach out to us at [vladimyr.kilko@gmail.com](mailto:vladimyr.kilko@gmail.com)
</div>
<div id="License">

## License

[MIT](LICENSE)
</div>