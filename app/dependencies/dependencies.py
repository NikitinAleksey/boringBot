from fastapi import Request

from bot.bot import BoringBot
from bot.features.menu.dispatcher import StrategyDispatcher
from bot.middlewares import get_bot_middlewares
from bot.routes import get_bot_routers

# MONGO_URI = CONFIGS['mongo'].get_uri()


# def create_container():
#     container = Container()
#     container.wire(modules=[dependencies.dependencies])
#     return container

async def setup_bot(
        bot_instance: BoringBot,
        strategy_dispatcher: StrategyDispatcher,
) -> None:
    routers = get_bot_routers()
    middlewares = get_bot_middlewares()
    bot_instance.register_routers(routers=routers)
    bot_instance.register_middlewares(middlewares=middlewares)


def get_bot_from_app(request: Request) -> BoringBot:
    return request.app.state.boring_bot


# @inject
# def create_bot(
#         bot_config: BotConfig = Provide[Container.bot_config],
# ) -> BoringBot:
#     bot = Bot(token=bot_config.BOT_TOKEN.get_secret_value())
#     dp = Dispatcher()
#     return BoringBot(bot=bot, dp=dp)
