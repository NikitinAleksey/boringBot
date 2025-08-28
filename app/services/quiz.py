import random
from datetime import datetime
from typing import Optional

from aiogram.fsm.context import FSMContext

from bot.features.menu.models import BotResponse
from database.respositories.interfaces import BaseMongoRepository
from external.interface import BaseAPI
from models.models import ItemModel, QuizModel, QuestionModel, TranslatedContentModel
from services.interface import BaseService
from services.parsers.interfaces import BaseQuizParser
from services.translator import BaseTranslator


class QuizService(BaseService):
    def __init__(self, translator: BaseTranslator, api_services: dict[str, BaseAPI],
                 repository: BaseMongoRepository, parser: BaseQuizParser):
        super().__init__(translator, api_services, repository)
        self.parser = parser

    async def get_item(self, state: Optional[FSMContext] = None):
        """
        Метод получения запрашиваемого объекта. В данном случае получает новый объект квиза.

        :param state: Опциональный параметр состояния, здесь нужен.
        :return: Текст ответа.
        """
        print(f'QuizService - get_item, state_type is {type(state)}')
        state_data = await state.get_data()
        current_quiz = state_data.get('quiz', {})

        if not current_quiz:
            print('No current quiz')
            api_service = self._get_service()
            resource = await api_service.get_resource()
            questions = self.parser.parse_object(data=resource, source=api_service.config.URL)
            normalized_questions = await self._prepare_questions(questions=questions, api_service=api_service)
            quiz_model = QuizModel(
                questions=normalized_questions,
                start_time=datetime.utcnow(),
            )
            await state.update_data({'quiz': quiz_model.dict(), 'question_index': 0})

        else:
            print(f'Have current quiz: {current_quiz}')
            questions = current_quiz.get('questions', [])
            question_index = state_data.get('question_index')
            question_index += 1
            if question_index < len(questions):
                await state.update_data({'question_index': question_index})
            else:
                quiz_model = self._calculate_results(quiz=current_quiz)
                quiz_dict = quiz_model.dict()
                # TODO тут по идее надо записывать результаты квиза (но у меня только 1 репозиторий, который не
                #  работает с коллекцией квизов, а только с вопросами - сиди и думай)
                await state.update_data({'quiz': quiz_dict, 'finished': True, 'question_index': None})

    def _normalize_item(
            self,
            new_object: Optional[QuestionModel],
            api_service: BaseAPI,
            current_object: Optional[dict],
    ) -> QuestionModel:
        """
        Приводит полученный item к модели
        :param new_object:
        :param api_service:
        :param current_object:
        :return:
        """
        if current_object:
            return QuestionModel(**current_object)

        translated_text = self.translator.translate(text=new_object.content.text)
        translated = TranslatedContentModel(
            text=translated_text,
            translated_by='google',
        )
        new_object.translated = translated
        return new_object

    def _get_service(self, api_service_name: Optional[str] = None) -> BaseAPI | None:
        """
        Выбирает случайный API сервис, если не передан api_service_name или сервиса
        с api_service_name не существует.

        :param api_service_name: Опциональное имя сервиса. Если не передан.
        :return: Выбранный сервис.
        """
        api_service = None
        if api_service_name:
            api_service = self.api_services.get(api_service_name)

        return api_service if api_service_name else random.choice(list(self.api_services.values()))

    async def _prepare_questions(self, questions:  list[QuestionModel], api_service: BaseAPI) -> list[QuestionModel]:
        """
        Проверяет, есть ли уже некоторые вопросы из списка в бд.
        Если есть, то не смысла их переводить повторно и тратить лимиты.
        Принимает решение, как обогатить модель вопроса переводом.

        :param questions: Список вопросов.
        :param api_service:
        :return: Список вопросов, обогащенный переводом.
        """
        titles = [question.title for question in questions]
        match = {'title': {'$in': titles}}
        cursor = await self.repository.read_many(match=match)
        questions_from_db = {}

        # Тут нормализуем. Все вопросы отсюда не требуют перевода - они все есть в базе.
        async for question in cursor:
            current_db_question = self._normalize_item(api_service=api_service, current_object=question, new_object=None)
            questions_from_db[question['title']] = current_db_question

        all_questions = []
        questions_to_save = []

        for question in questions:
            if question.title in questions_from_db:
                all_questions.append(questions_from_db[question.title])
            else:
                current_question = self._normalize_item(new_object=question, api_service=api_service, current_object=None)
                questions_to_save.append(current_question.model_dump(exclude_none=True))

        await self.repository.insert_many(query=questions_to_save)
        return all_questions

    @staticmethod
    def _calculate_results(quiz: dict) -> QuizModel:
        """
        Подсчитывает результаты квиза.

        :param quiz: Модель завершенного квиза.
        :return: Обогащенная модель с результатами.
        """
        quiz = QuizModel(**quiz)

        total_answered = 0
        total_correct = 0

        for question in quiz.questions:
            total_answered += 1
            if question.correct_answer == question.user_answer:
                total_correct += 1

        quiz.answered_count = total_answered
        quiz.correct_count = total_correct
        return quiz
