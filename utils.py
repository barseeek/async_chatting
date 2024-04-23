import datetime
import logging

from contextlib import asynccontextmanager

import asyncio
import aiofiles


logger = logging.getLogger('sender')


@asynccontextmanager
async def get_connection(host, port, filename, attempts=3, timeout=5):
    writer = None
    attempts_count = 0
    reader = None
    while not reader:
        try:
            reader, writer = await asyncio.open_connection(
                host, port)
            logger.info('Connection established\n')
            yield reader, writer
        except ConnectionError:
            if attempts_count < attempts:
                logger.info('Connection Error, try again\n')
                if filename:
                    await handle_output(filename, 'Connection Error, try again\n')
                attempts_count += 1
                continue
            else:
                logger.info(f'{attempts} Connection Error in a row, try again in {timeout} secs\n')
                if filename:
                    await handle_output(filename, 'Connection Error, try again\n')
                await asyncio.sleep(timeout)
        finally:
            if writer:
                writer.close()
                await writer.wait_closed()


async def handle_output(file, message):
    formatted_datetime = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
    text = f'[{formatted_datetime}]: {message}'
    async with aiofiles.open(file, mode='a') as f:
        await f.write(text)
    print(text)
