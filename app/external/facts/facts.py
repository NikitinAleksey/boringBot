import random

from aiohttp import ClientSession

from core.configs.external_api_config import NumbersAPIConfig
from external.interface import BaseAPI


class NumbersAPI(BaseAPI):
    def __init__(self, config: NumbersAPIConfig):
        super().__init__(config)

    async def get_resource(self):
        """

        :return:
        """
        url = self.config.URL + '/random' + self._make_choice()
        async with ClientSession() as client:
            response = await client.get(url=url)
            return await response.text()

    @staticmethod
    def _make_choice() -> str:
        variables = ['/trivia', '/year', '/date', '/math']
        return random.choice(variables)
