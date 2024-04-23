import datetime

from contextlib import asynccontextmanager

import asyncio
import aiofiles


@asynccontextmanager
async def get_connection(host, port, filename, attempts=3, timeout=5):
    writer = None
    attempts_count = 0
    while True:
        try:
            reader, writer = await asyncio.open_connection(
                host, port)
            await handle_output(filename, 'Установлено соединение\n')
            yield reader, writer
        except ConnectionError:
            if attempts_count < attempts:
                if filename:
                    await handle_output(filename, 'Connection Error, try again')
                attempts_count += 1
                continue
            else:
                if filename:
                    await handle_output(filename, f'{attempts} Connection Error in a row, try again in {timeout} secs')
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
