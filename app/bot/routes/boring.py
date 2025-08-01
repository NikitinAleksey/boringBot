from typing import Union

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.features.menu.dispatcher import StrategyDispatcher
from bot.fsm.states import MenuState

boring_router = Router()


@boring_router.callback_query(F.data == "fact")
async def fact_handler(
        event: Union[Message, CallbackQuery],
        state: FSMContext,
        strategy_dispatcher: StrategyDispatcher,):
    """
    Обработчик коллбэка с текстом boring.

    :param event: Сообщение или CallbackQuery.
    :param state: Контекст состояния FSM.
    :param strategy_dispatcher: Диспетчер стратегий выбора текстов и кнопок.
    :return: Ответное сообщение.
    """
    await state.set_state(MenuState.fact)
    message = event if isinstance(event, Message) else event.message
    response = await strategy_dispatcher.dispatch(event, state)

    return await message.edit_text(
        text=response.text,
        reply_markup=response.kb,
    )
