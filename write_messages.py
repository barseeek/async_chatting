import argparse
import json
import logging

import asyncio

from utils import get_connection


logger = logging.getLogger('sender')


def parse_args():
    parser = argparse.ArgumentParser(description="Async chat listener")
    parser.add_argument("-l", "--logging", action='store_true')
    parser.add_argument("-ho", "--host", type=str, default='minechat.dvmn.org',
                        help="Set the host address")
    parser.add_argument("-p", "--port", type=int, default=5050,
                        help="Set the port number on which you want to write messages")
    parser.add_argument("-f", "--filepath", type=str, default="messages.txt",
                        help="Set path to the file where the messages will be written to")
    parser.add_argument("-t", "--token", type=str, default="",
                        help="Set your token")
    parser.add_argument("-m", "--message", type=str, default="Test message",
                        help="Set your message")
    parser.add_argument("-n", "--name", type=str, default="Anonymous",
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


async def main():
    args = parse_args()
    if args.logging:
        logging.basicConfig(level=logging.DEBUG)
    host = args.host
    port = args.port
    filename = args.filepath
    token = args.token
    async with get_connection(host, port, filename, attempts=3, timeout=5) as (reader, writer):
        if token:
            auth = await is_token_valid(token, reader, writer)
            if not auth:
                logger.error('Non-valid token, check it and try again')
        else:
            message = await read_message(reader)
            await write_message(writer)
            message = await read_message(reader)
            await write_message(writer, 'Nikita\n')
            message = await read_message(reader)
        await write_message(writer, 'test message\n\n')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
