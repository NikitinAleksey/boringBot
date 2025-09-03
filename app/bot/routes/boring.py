from typing import Union

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dependency_injector.wiring import Provide, inject

from bot.features.menu.dispatcher import StrategyDispatcher
from bot.fsm.states import MenuState
from dependencies.container import Container

boring_router = Router()


@boring_router.callback_query(F.data == "fact")
@inject
async def fact_handler(
        event: Union[Message, CallbackQuery],
        state: FSMContext,
        strategy_dispatcher: StrategyDispatcher = Provide[Container.strategy_dispatcher],
):
    """
    Обработчик коллбэка с текстом fact.

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


@boring_router.callback_query(F.data == "joke")
@inject
async def joke_handler(
        event: Union[Message, CallbackQuery],
        state: FSMContext,
        strategy_dispatcher: StrategyDispatcher = Provide[Container.strategy_dispatcher],
):
    """
    Обработчик коллбэка с текстом joke.

    :param event: Сообщение или CallbackQuery.
    :param state: Контекст состояния FSM.
    :param strategy_dispatcher: Диспетчер стратегий выбора текстов и кнопок.
    :return: Ответное сообщение.
    """
    await state.set_state(MenuState.joke)
    message = event if isinstance(event, Message) else event.message
    response = await strategy_dispatcher.dispatch(event, state)
    print('RESPONSE ')
    print(response)
    return await message.edit_text(
        text=response.text,
        reply_markup=response.kb,
    )


@boring_router.callback_query(F.data == "quiz")
@inject
async def quiz_handler(
        event: Union[Message, CallbackQuery],
        state: FSMContext,
        strategy_dispatcher: StrategyDispatcher = Provide[Container.strategy_dispatcher],
):
    """
    Обработчик коллбэка с текстом quiz и всего процесса квиза.

    :param event: Сообщение или CallbackQuery.
    :param state: Контекст состояния FSM.
    :param strategy_dispatcher: Диспетчер стратегий выбора текстов и кнопок.
    :return: Ответное сообщение.
    """
    print('Quiz handler')
    print(type(state))
    await state.set_state(MenuState.quiz)
    await state.set_data({})
    message = event if isinstance(event, Message) else event.message
    response = await strategy_dispatcher.dispatch(event=event, state=state)
    print('RESPONSE ')
    print(response)
    return await message.edit_text(
        text=response.text,
        reply_markup=response.kb,
    )


@boring_router.callback_query(StateFilter(MenuState.quiz))
@inject
async def quiz_process_handler(
        event: Union[Message, CallbackQuery],
        state: FSMContext,
        strategy_dispatcher: StrategyDispatcher = Provide[Container.strategy_dispatcher],
):
    """
    Обработчик всего процесса квиза.

    :param event: Сообщение или CallbackQuery.
    :param state: Контекст состояния FSM.
    :param strategy_dispatcher: Диспетчер стратегий выбора текстов и кнопок.
    :return: Ответное сообщение.
    """
    print('Quiz process handler')
    print(type(state))
    await state.update_data({'answer': event.data})
    message = event if isinstance(event, Message) else event.message
    response = await strategy_dispatcher.dispatch(event=event, state=state)
    print('RESPONSE ')
    print(response)
    return await message.edit_text(
        text=response.text,
        reply_markup=response.kb,
    )
