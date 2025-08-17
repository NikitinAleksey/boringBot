from typing import Union

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dependency_injector.wiring import inject, Provide

from bot.features.menu.dispatcher import StrategyDispatcher
from bot.fsm.states import MenuState
from dependencies.container import Container

commands_router = Router()


@commands_router.callback_query(F.data == "start")
@commands_router.message(CommandStart())
@inject
async def start_handler(
        event: Union[Message, CallbackQuery],
        state: FSMContext,
        strategy_dispatcher: StrategyDispatcher = Provide[Container.strategy_dispatcher],
):
    """
    Обработчик команды /start или коллбэка с текстом start.

    :param event: Сообщение или CallbackQuery.
    :param state: Контекст состояния FSM.
    :param strategy_dispatcher: Диспетчер стратегий выбора текстов и кнопок.
    :return: Ответное сообщение.
    """
    await state.set_state(MenuState.start)
    message = event if isinstance(event, Message) else event.message

    response = await strategy_dispatcher.dispatch(event, state)

    data = await state.get_data()
    main_message = data.get('main_message')
    if main_message:
        await main_message.edit_text(
            text=response.text,
            reply_markup=response.kb,
        )
    else:
        main_message = await message.answer(
            text=response.text,
            reply_markup=response.kb,
        )
        await state.update_data({'main_message': main_message})


@commands_router.callback_query(F.data == "main_menu")
@commands_router.message(F.data == "main_menu")
@inject
async def menu_handler(
        event: Union[Message, CallbackQuery],
        state: FSMContext,
        strategy_dispatcher: StrategyDispatcher = Provide[Container.strategy_dispatcher],
):
    """
    Обработчик команды /main_menu или коллбэка с текстом start.

    :param event: Сообщение или CallbackQuery.
    :param state: Контекст состояния FSM.
    :param strategy_dispatcher: Диспетчер стратегий выбора текстов и кнопок.
    :return: Ответное сообщение.
    """
    print('menu_handler')
    await state.set_state(MenuState.main)
    response = await strategy_dispatcher.dispatch(event, state)
    data = await state.get_data()
    current_message = event if isinstance(event, Message) else event.message
    main_message = data.get('main_message', current_message)
    return await main_message.edit_text(
        text=response.text,
        reply_markup=response.kb,
    )
