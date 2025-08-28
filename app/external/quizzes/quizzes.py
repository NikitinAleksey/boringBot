from aiohttp import ClientSession

from core.configs.external_api_config import OpenTdbAPIConfig
from external.interface import BaseAPI


class OpenTdbAPI(BaseAPI):
    def __init__(self, config: OpenTdbAPIConfig):
        super().__init__(config)

    async def get_resource(self):
        # TODO щаложить расширяемость с помощью кваргов в этом методе на уровне интерфейса - они будет полезны все, а
        #  не только здесь. А пока хардкод!!!!! amount, type, category, difficulty
        url = self.config.URL + '/api.php?' + 'amount=10&type=multiple' # это и есть хардкод
        async with ClientSession() as client:
            resp = await client.get(url=url)
            data = await resp.json()
            return data
