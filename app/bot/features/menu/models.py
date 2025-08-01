from pydantic import BaseModel, Field
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


class BotResponse(BaseModel):
    text: str = Field(description='Текст ответа бота.')
    kb: InlineKeyboardMarkup | ReplyKeyboardMarkup = Field(default=None, description='Клавиатура ответа.')
