from aiohttp import ClientSession

from core.configs.external_api_config import RandomJokeAPIConfig, DadJokeAPIConfig, ChuckNorrisAPIConfig
from external.interface import BaseAPI


class RandomJokeAPI(BaseAPI):
    def __init__(self, config: RandomJokeAPIConfig):
        super().__init__(config)

    async def get_resource(self) -> str:
        url = self.config.URL + '/joke/Any'
        async with ClientSession() as client:
            response = await client.get(url=url)
            content = await response.json()
            print(content)
            return content.get('setup') + ' ' + content.get('delivery')


class DadJokeAPI(BaseAPI):
    def __init__(self, config: DadJokeAPIConfig):
        super().__init__(config)

    async def get_resource(self):
        async with ClientSession() as client:
            resp = await client.get(
                url=self.config.URL,
                headers={"Accept": "application/json"}
            )
            data = await resp.json()
            return data.get("joke", "")


class ChuckNorrisAPI(BaseAPI):
    def __init__(self, config: ChuckNorrisAPIConfig):
        super().__init__(config)

    async def get_resource(self):
        url = self.config.URL + '/jokes/random'
        async with ClientSession() as client:
            resp = await client.get(url=url)
            data = await resp.json()
            return data.get("value")
