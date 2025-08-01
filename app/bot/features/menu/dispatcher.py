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
            keyboard_factory: BaseKeyboardFactory,
            text_extractor: TextExtractor,
            service: BaseService,
    ):
        self.strategies = strategies
        self.keyboard_factory = keyboard_factory
        self.text_extractor = text_extractor
        self.service = service

    async def dispatch(self, event: Union[Message, CallbackQuery], state: FSMContext) -> BotResponse | None:
        print('dispatch')
        current_state = await state.get_state()
        print(current_state)
        strategy = self.strategies.get(current_state)
        print(strategy)
        if strategy:
            strategy_result = await strategy.execute(
                event=event, state=state, keyboard_factory=self.keyboard_factory, text_extractor=self.text_extractor,
                service=self.service,
            )
            return strategy_result
        print('No strategy')
