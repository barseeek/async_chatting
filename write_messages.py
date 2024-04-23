import argparse
import json
import logging

import aioconsole
import asyncio

from environs import Env
from utils import get_connection


logger = logging.getLogger('sender')


def parse_args():
    env = Env()
    env.read_env()
    parser = argparse.ArgumentParser(description="Async chat writer")
    parser.add_argument("-l", "--logging", action='store_true')
    parser.add_argument("-ho", "--host", type=str,
                        default=env.str('HOST', 'minechat.dvmn.org'),
                        help="Set the host address")
    parser.add_argument("-p", "--port", type=int,
                        default=env.int('PORT_WRITER', 5050),
                        help="Set the port number on which you want to write messages")
    parser.add_argument("-f", "--filepath", type=str,
                        default=env.str('FILE_PATH', 'messages.txt'),
                        help="Set path to the file where the messages will be written to")
    parser.add_argument("-t", "--token", type=str,
                        default=env.str('CHAT_TOKEN', ''),
                        help="Set your token")
    parser.add_argument("-m", "--message", type=str,
                        help="Set your message")
    parser.add_argument("-n", "--name", type=str,
                        default=env.str('USERNAME', 'Anonymous'),
                        help="Set your nickname")
    return parser.parse_args()


async def read_message(reader):
    data = await reader.readline()
    message = data.decode().rstrip('\n')
    logger.debug(message)
    return message


async def write_message(writer, message=None):
    if not message:
        message = '\n'
    writer.write(message.encode())
    logger.debug(message)
    await writer.drain()


async def is_token_valid(token, reader, writer):
    message = await read_message(reader)
    await write_message(writer, f'{token}\n')
    message = await read_message(reader)
    if json.loads(message):
        return True
    return False


async def submit_message(writer, message):
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()


async def register_user(username, reader, writer):
    await read_message(reader)
    await write_message(writer)
    await read_message(reader)
    if username:
        await write_message(writer, f'{username}\n')
    else:
        await write_message(writer)
    account_data = await read_message(reader)
    return json.loads(account_data)


async def get_messages(writer):
    while True:
        message = await aioconsole.ainput('Enter your message: ')
        await submit_message(writer, message)


async def main():
    args = parse_args()
    if args.logging:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.disable(logging.CRITICAL)
    host = args.host
    port = args.port
    filename = args.filepath
    token = args.token
    username = args.name
    message = args.message
    async with get_connection(host, port, filename, attempts=3, timeout=5) as (reader, writer):
        if token:
            if not await is_token_valid(token, reader, writer):
                logger.error('Non-valid token, check it and try again')
        else:
            await register_user(username, reader, writer)
        if message:
            await submit_message(writer, message)
        else:
            await get_messages(writer)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
