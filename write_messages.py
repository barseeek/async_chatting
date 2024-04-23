import argparse

import asyncio

from utils import get_connection


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
    return message


async def write_message(writer, message=None):
    if not message:
        message = '\n'
    writer.write(message.encode())
    await writer.drain()


async def main():
    args = parse_args()
    host = args.host
    port = args.port
    filename = args.filepath
    token = args.token
    async with get_connection(host, port, filename, attempts=3, timeout=5) as (reader, writer):
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
