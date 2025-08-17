import asyncio

import aiohttp
from pyngrok import ngrok

from core.configs.ngrok_config import NgrokConfig


class LaunchNgrok:
    def __init__(self, config: NgrokConfig):
        self.token = config.NGROK_AUTHTOKEN
        self.port = config.NGROK_PORT
        self.public_url = None

    def connect(self):
        print('try to kill')
        ngrok.kill()
        print(f'try to set token')
        ngrok.set_auth_token(token=self.token.get_secret_value())
        print('try to connect')
        self.public_url = ngrok.connect(self.port).public_url

    def disconnect(self):
        if self.public_url:
            ngrok.disconnect(self.public_url)
            self.public_url = None

    async def wait_until_available(self, timeout: int = 10):
        for _ in range(timeout * 2):  # timeout секунд, шаг 0.5с
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.public_url) as resp:
                        if resp.status < 500:  # уже отвечает хоть как-то
                            return
            except Exception:
                pass
            await asyncio.sleep(0.5)
        raise TimeoutError(f"{self.public_url} not available after {timeout} seconds")