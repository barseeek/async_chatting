# Скрипты для общения в чате
Скрипты позволяют подключаться к чату, сохранять историю переписки и отправлять в него сообщения.

## Как установить
Для работы утилиты нужен Python версии не ниже 3.7.
1. Клонирование репозитория
```bash
git clone https://github.com/barseeek/async_chatting.git
```

#### 2. Установка необходимых библиотек Python
```bash
pip install -r requirements.txt
```

## Аргументы командной строки:

```bash 
usage: write_messages.py [-h] [-l] [-ho HOST] [-p PORT] [-f FILEPATH] [-t TOKEN] [-m MESSAGE] [-n NAME]

Async chat writer

options:
  -h, --help            show this help message and exit
  -ho HOST, --host HOST Set the host address
  -p PORT, --port PORT  Set the port number on which you want to write messages
  -f FILEPATH, --filepath FILEPATH
                        Set path to the file where the messages will be written to
  -t TOKEN, --token TOKEN
                        Set your token
  -m MESSAGE, --message MESSAGE
                        Set your message
  -n NAME, --name NAME  Set your nickname
```
```bash
usage: listen_messages.py [-h] [-l] [-ho HOST] [-p PORT] [-f FILEPATH]

Async chat listener

options:
  -h, --help            show this help message and exit
  -l, --logging
  -ho HOST, --host HOST
                        Set the host address
  -p PORT, --port PORT  Set the port number on which you want to listen to messages
  -f FILEPATH, --filepath FILEPATH
                        Set path to the file where the messages will be written to
```
## Переменные окружения
`HOST` - адрес чата. По умолчанию `minechat.dvmn.org`.

`PORT_LISTENER` - порт для прослушивания сообщений чата. По умолчанию 5000.

`PORT_WRITER` - порт для отправки сообщений в чат. По умолчанию 5050.

`FILE_PATH` - путь до файла, куда записывается история сообщений. По умолчанию `messages.txt`.

`USERNAME` - имя пользователя, по умолчанию `Anonymous`.

`CHAT_TOKEN` - токен пользователя. Если токена нет, регистрируем нового пользователя с ником `USERNAME`.

`ACCOUNT_HASH` - токен пользователя. По умолчанию пустой токен (будет зарегистрирован новый пользователь).

## Как запустить

Скрипт прослушивания чата запускают со следующими необязательными параметрами:

`--host`  - адрес чата.

`--port` - порт для прослушивания сообщений чата.

`--filepath` - путь до файла, куда записывается история сообщений. 


Например:
```bash
python3 listen_messages.py
```

Скрипт для регистрации в чате и отправки сообщений в чат запускают со следующими необязательными параметрами:

`--host`  - адрес чата.

`--port` - порт для прослушивания сообщений чата.

`--filepath` - путь до файла, куда записывается история сообщений. 

`--token` - токен пользователя.

`--name` - имя пользователя.

`--message` - текст сообщения.


```bash
python3 write_messages.py --user Nikita --message test
```

