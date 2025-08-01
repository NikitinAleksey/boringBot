from bot.routes.commands import commands_router
from bot.routes.boring import boring_router


def get_bot_routers():
    # Здесь добавляем все роутеры бота
    return [commands_router, boring_router]
