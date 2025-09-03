from aiohttp import ClientSession

from core.configs.external_api_config import OpenTdbAPIConfig
from external.interface import BaseAPI


class OpenTdbAPI(BaseAPI):
    def __init__(self, config: OpenTdbAPIConfig):
        super().__init__(config)

    async def get_resource(self):
        url = self.config.URL + '/api.php?' + 'amount=10&type=multiple' # это хардкод, надо исправить
        async with ClientSession() as client:
            resp = await client.get(url=url)
            data = await resp.json()
            return data

# async def main():
#     url = 'https://opentdb.com/api.php?amount=10&type=multiple'
#     async with ClientSession() as client:
#         resp = await client.get(url=url)
#         data = await resp.json()
#         print(data)
#
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
