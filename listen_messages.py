import argparse
import logging

import asyncio

from environs import Env
from utils import get_connection, handle_output

logger = logging.getLogger('listener')


async def read_messages(host, port, filename):
    async with get_connection(host, port, filename, attempts=3, timeout=5) as (reader, writer):
        try:
            while True:
                message = await reader.readline()
                if not message:
                    continue
                await handle_output(filename, f'{message.decode()}')
        except ConnectionError:
            logger.error('Connection Error')


def parse_args():
    env = Env()
    env.read_env()
    parser = argparse.ArgumentParser(description="Async chat listener")
    parser.add_argument("-ho", "--host", type=str,
                        default=env.str('HOST', 'minechat.dvmn.org'),
                        help="Set the host address")
    parser.add_argument("-p", "--port", type=int,
                        default=env.int('PORT_LISTENER', 5000),
                        help="Set the port number on which you want to listen to messages")
    parser.add_argument("-f", "--filepath", type=str,
                        default=env.str('FILE_PATH', 'messages.txt'),
                        help="Set path to the file where the messages will be written to")
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    try:
        asyncio.run(read_messages(args.host, args.port, args.filepath))
    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt')