import html

from models.models import QuestionModel, ContentModel
from services.parsers.parser_interfaces import BaseQuizParser


class OpenTDBParser(BaseQuizParser):
    def parse_object(self, data: dict, source: str) -> list[QuestionModel]:
        """
        Парсит json от своего АПИ, приводя его к списку моделей вопросов.

        :param data: Сырые данные.
        :param source: Источник.
        :return: Список вопросов для квиза.
        """
        questions = data.get('results', [])
        question_models = []

        for question in questions:
            category = html.unescape(question.get('category'))
            correct_answer = html.unescape(question.get('correct_answer'))
            incorrect_answers = [html.unescape(answer) for answer in question.get('incorrect_answers')]
            question = html.unescape(question.get('question'))

            content = ContentModel(text=question)
            question_model = QuestionModel(
                title=" ".join(question.split()[:5]),
                content=content,
                topics=[category],
                source=source,
                correct_answer=correct_answer,
                answers=incorrect_answers + [correct_answer]
            )
            question_models.append(question_model)

        return question_models
