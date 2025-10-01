import random

from aiohttp import ClientSession

from core.configs.external_api_config import NumbersAPIConfig, CatsNinjaAPIConfig, UselessFactsAPIConfig, \
    MeowFactsAPIConfig
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


class CatsNinjaAPI(BaseAPI):
    def __init__(self, config: CatsNinjaAPIConfig):
        super().__init__(config)

    async def get_resource(self):
        """

        :return:
        """
        url = self.config.URL + '/fact'
        async with ClientSession() as client:
            response = await client.get(url=url)
            content = await response.json()
            return content.get('fact')


class UselessFactsAPI(BaseAPI):
    def __init__(self, config: UselessFactsAPIConfig):
        super().__init__(config)

    async def get_resource(self):
        url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
        async with ClientSession() as client:
            response = await client.get(url=url)
            content = await response.json()
            return content.get('text')


class MeowFactsAPI(BaseAPI):
    def __init__(self, config: MeowFactsAPIConfig):
        super().__init__(config)

    async def get_resource(self):
        url = self.config.URL
        async with ClientSession() as client:
            response = await client.get(url=url)
            content = await response.json()
            return content.get("data", [""])[0]
