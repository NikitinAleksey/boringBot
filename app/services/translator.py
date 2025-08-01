from deep_translator import GoogleTranslator
from google.cloud import translate_v2
from google.oauth2 import service_account

from core.configs.translators_configs import GoogleTranslatorConfig

translator = GoogleTranslator(source='auto', target='ru')


class GoogleTranslator:
    def __init__(self, config: GoogleTranslatorConfig):
        self.client = translate_v2.Client(
            credentials=service_account.Credentials.from_service_account_file(
                filename=config.GOOGLE_APPLICATION_CREDENTIALS,
            )
        )

    def translate(self, text: str, target_lang: str = "ru") -> str:
        result = self.client.translate(text, target_language=target_lang)
        return result["translatedText"]
