from aiogram.fsm.state import StatesGroup, State


class MenuState(StatesGroup):
    start = State()
    main = State()
    joke = State()
    fact = State()
    youtube = State()
