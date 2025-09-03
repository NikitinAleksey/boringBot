from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field

from core.paths import BASE_DIR


class MongoConfig(BaseSettings):
    # Database params
    USER: SecretStr = Field(..., alias="MONGO_INITDB_ROOT_USERNAME")
    PASSWORD: SecretStr = Field(..., alias="MONGO_INITDB_ROOT_PASSWORD")
    HOST: str = Field(..., alias="MONGO_HOST")
    PORT: int = Field(..., alias="MONGO_PORT")

    # Databases
    DB_NAME: str = Field(description='Название основной бд')

    # Collections
    FACTS: str = Field(description='Название коллекции с фактами')
    JOKES: str = Field(description='Название коллекции с шутками')
    VIDEOS: str = Field(description='Название коллекции с видео')
    QUIZZES: str = Field(description='Название коллекции с результатами квизов')
    QUESTIONS: str = Field(description='Название коллекции с вопросами для квизов')

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    def get_uri(self) -> str:
        return f'mongodb://{self.USER.get_secret_value()}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/'
