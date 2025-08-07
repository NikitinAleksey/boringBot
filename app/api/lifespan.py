from contextlib import asynccontextmanager

from fastapi import FastAPI
from dependencies.dependencies import get_ngrok, create_bot, setup_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    ngrok_instance = get_ngrok()
    try:
        ngrok_instance.connect()
    except Exception as exc:
        ngrok_instance.disconnect()
    finally:
        ngrok_instance.connect()

    bot = create_bot()
    app.state.boring_bot = bot
    await setup_bot(bot_instance=bot)
    print(ngrok_instance.public_url + '/tg_hook')
    await bot.set_webhook(url=ngrok_instance.public_url + '/tg_hook')
    yield
    ngrok_instance.disconnect()
    await bot.delete_webhook()
