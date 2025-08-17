from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.features.menu.strategies import BaseStrategy
from bot.features.menu.models import BotResponse
from bot.keyboards.builders import BaseKeyboardFactory
from bot.static.text_extractor import TextExtractor
from services.interface import BaseService


class StrategyDispatcher:
    def __init__(
            self,
            strategies: dict[str, BaseStrategy],
    ):
        self.strategies = strategies

    async def dispatch(self, event: Union[Message, CallbackQuery], state: FSMContext) -> BotResponse | None:
        print('dispatch')
        current_state = await state.get_state()
        print(current_state)
        strategy = self.strategies.get(current_state)
        print('==============================================')
        print(strategy)
        print('==============================================')

        if strategy:
            strategy_result = await strategy().execute(event=event)
            return strategy_result
        print('No strategy')
