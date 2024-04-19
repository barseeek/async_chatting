import argparse

import asyncio

from utils import get_connection, handle_output


async def write_messages(host, port, filename, token, username):
    async with get_connection(host, port, filename, attempts=3, timeout=5) as (reader, writer):
        try:
            while True:
                message = await reader.readline()
                if not message:
                    continue
                await handle_output(filename, f'{message.decode()}')
        except ConnectionError:
            pass


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


if __name__ == '__main__':
    args = parse_args()

    asyncio.run(write_messages(args.host, args.port, args.filepath, args.token, args.name))
