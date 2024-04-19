import asyncio
import aiofiles
import datetime


async def handle_output(message):
    formatted_datetime = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
    text = f'[{formatted_datetime}]: {message}'
    async with aiofiles.open('test.txt', mode='a') as f:
        await f.write(text)
    print(text)


async def tcp_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)
    await handle_output('Установлено соединение\n')
    try:
        while True:
            data = await reader.readline()
            await handle_output(f'{data.decode()}')
    except ConnectionError:
        pass


asyncio.run(tcp_client())
