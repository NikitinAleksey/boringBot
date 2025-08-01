from aiogram import Router, BaseMiddleware, Bot, Dispatcher


class BoringBot:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        self.webhook = None

    async def set_webhook(self, url: str) -> None:
        """
        Устанавливает ссылку на веб хук бота.

        :param url: URL эндпоинта.
        :return: None
        """
        if not self.webhook:
            self.webhook = url
            await self.bot.set_webhook(url=self.webhook)

    async def delete_webhook(self) -> None:
        """
        Удаляет веб хук бота.

        :return: None
        """
        if self.webhook:
            self.webhook = None
            await self.bot.delete_webhook(drop_pending_updates=True)

    def register_middlewares(self, middlewares: list[BaseMiddleware]) -> None:
        """
        Регистрирует миддлвары в диспетчере.

        :param middlewares: Список миддлваров для регистрации.
        :return: None
        """
        for middleware in middlewares:
            self.dp.update.middleware(middleware)

    def register_routers(self, routers: list[Router]) -> None:
        """
        Регистрирует роутеры в диспетчере.

        :param routers: Список роутеров для регистрации.
        :return: None
        """
        for router in routers:
            self.dp.include_router(router=router)
