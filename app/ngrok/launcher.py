from pyngrok import ngrok

from core.configs.ngrok_config import NgrokConfig


class LaunchNgrok:
    def __init__(self, config: NgrokConfig):
        self.token = config.NGROK_TOKEN
        self.port = config.NGROK_PORT
        self.public_url = None

    def connect(self):
        ngrok.kill()
        ngrok.set_auth_token(token=self.token.get_secret_value())
        self.public_url = ngrok.connect(self.port).public_url

    def disconnect(self):
        if self.public_url:
            ngrok.disconnect(self.public_url)
            self.public_url = None
