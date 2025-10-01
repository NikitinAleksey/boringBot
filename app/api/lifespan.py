from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot.routes import boring
from bot.routes import commands
import dependencies.dependencies as deps
from dependencies.container import Container
from dependencies.dependencies import setup_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    container = Container()
    print('Container created')
    container.wire(modules=[deps, boring, commands])
    print('Creating bot')
    bot = container.bot()
    print('BOt created')

    app.state.boring_bot = bot
    app.state.container = container

    await setup_bot(bot_instance=bot, strategy_dispatcher=container.strategy_dispatcher)
    # print(ngrok_instance.public_url + '/tg_hook')
    # await ngrok_instance.wait_until_available()
    await bot.set_webhook(url='https://briefs-alexandria-nomination-safe.trycloudflare.com/tg_hook')
    print('START UP IS COMPLETED')
    yield
    # ngrok_instance.disconnect()
    await bot.delete_webhook()
