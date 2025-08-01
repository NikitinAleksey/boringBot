from typing import Annotated

from aiogram.types import Update
from fastapi import APIRouter, Depends, Request

from bot.bot import BoringBot
from dependencies.dependencies import get_bot_from_app

router = APIRouter()


@router.post('/tg_hook')
async def tg_hook(
        request: Request,
        bot: Annotated[BoringBot, Depends(get_bot_from_app)],
) -> dict:
    data = await request.json()
    print(data)
    update = Update.model_validate(data)

    await bot.dp.feed_update(bot.bot, update)
    return {"status": "ok"}
