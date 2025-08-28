from abc import ABC, abstractmethod
from typing import Union, Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.features.menu.models import BotResponse
from bot.keyboards.builders import BaseKeyboardFactory
from bot.static.text_extractor import TextExtractor
from external.interface import BaseAPI
from models.models import QuizModel
from services.interface import BaseService


class BaseStrategy(ABC):
    """Базовый интерфейс стратегий меню."""
    def __init__(
            self,
            keyboard_factory: BaseKeyboardFactory,
            text_extractor: TextExtractor,
            service: Optional[BaseService] = None,
            state: Optional[FSMContext] = None,
    ):
        self.keyboard_factory = keyboard_factory
        self.text_extractor = text_extractor
        self.service = service
        self.state = state

    @abstractmethod
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            state: Optional[FSMContext] = None,
    ) -> BotResponse:
        """
        Все потомки обязаны реализовать этот метод.

        :param event: Событие в боте.
        :param state: Состояние. Важно не для всех стратегий.
        :returns: Ответ пользователю.
        """
        pass


class StartStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            state: Optional[FSMContext] = None,
    ) -> BotResponse:
        """
        Стратегия отображения меню по нажатию кнопки старт.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :param state: Состояние. Важно не для всех стратегий.
        :returns: Ответ пользователю.
        """
        print('StartStrategy')
        name = event.from_user.first_name
        text = self.text_extractor.get_text(key="start", name=name)
        buttons = self.text_extractor.get_buttons(key="start")
        kb = self.keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class MainMenuStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            state: Optional[FSMContext] = None,
    ) -> BotResponse:
        """
        Стратегия отображения главного меню.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :param state: Состояние. Важно не для всех стратегий.
        :returns: Ответ пользователю.
        """
        print('MainMenuStrategy')
        name = event.from_user.first_name
        text = self.text_extractor.get_text(key="main_menu", name=name)
        buttons = self.text_extractor.get_buttons(key="main_menu")
        kb = self.keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class FactStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            state: Optional[FSMContext] = None,
    ) -> BotResponse:
        """
        Стратегия отображения получения интересного факта. Факт получает из своего сервиса.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :param state: Состояние. Важно не для всех стратегий.
        :returns: Ответ пользователю.
        """
        print('FactStrategy')
        name = event.from_user.first_name
        preview_text = self.text_extractor.get_text(key="fact", name=name)
        main_text = await self.service.get_item()
        text = preview_text + '\n\n' + main_text
        buttons = self.text_extractor.get_buttons(key="fact")
        kb = self.keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class JokeStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            state: Optional[FSMContext] = None,
    ) -> BotResponse:
        """
        Стратегия отображения получения шуток. Шутку получает из своего сервиса.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :param state: Состояние. Важно не для всех стратегий.
        :returns: Ответ пользователю.
        """
        print('JokeStrategy')
        name = event.from_user.first_name
        preview_text = self.text_extractor.get_text(key="joke", name=name)
        main_text = await self.service.get_item()
        text = preview_text + '\n\n' + main_text
        buttons = self.text_extractor.get_buttons(key="joke")
        kb = self.keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class QuizStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            state: Optional[FSMContext] = None,
    ) -> BotResponse:
        """
        Стратегия отображения получения викторин. Викторину получает из своего сервиса.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :param state: Состояние. В этой стратегии состояние важно.
        :returns: Ответ пользователю.
        """
        print('QuizStrategy')
        name = event.from_user.first_name
        preview_text = self.text_extractor.get_text(key="quiz", name=name)
        await self.service.get_item(state=state)
        main_text, buttons = await self._extract_data(state=state)

        text = preview_text + '\n\n' + main_text
        kb = self.keyboard_factory.create(buttons=buttons, adjust=2)
        return BotResponse(text=text, kb=kb)

    @staticmethod
    async def _extract_data(state: FSMContext):
        """

        :param state:
        :return:
        """
        data = await state.get_data()
        quiz = data.get('quiz')
        quiz = QuizModel(**quiz) # TODO тут аккуратнее, вдруг не будет квиза, обработать
        question_index = data.get('question_index')
        is_finished = data.get('finished')
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(quiz)
        print(question_index)
        print(is_finished)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        if quiz and is_finished:
            text = f'Завершен. Отвечено правильно {quiz.correct_count}/{quiz.answered_count}'
            buttons = [['Начать заново', 'quiz']] # Естественно это и текст в json перевести
        elif quiz and question_index is not None:
            print('QUESTIONS')
            for q in quiz.questions:
                print(q)
            questions = quiz.questions
            question = questions[question_index]
            text = question.translated.text
            buttons = [[answer, answer] for answer in question.answers]
        else:
            text = 'Fuck error'
            buttons = [['Suck my dick', 'quiz']]
        return text, buttons

    # TODO
    #  1 ЗАпустился квиз
    #  2 Надо обрабатывать ответы и записывать их, в СОСТОЯНИЕ? - наверное
    #  3 Ответы не переведены - это плохо
    #  4 В стратегии только 1 репозиторий, надо найти способ записи в нужную коллекцию с помощью одного репозитория