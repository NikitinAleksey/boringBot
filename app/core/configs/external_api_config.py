from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.paths import BASE_DIR


class BaseAPIConfig(BaseSettings):
    URL: str = Field(default='')

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


# Facts
class NumbersAPIConfig(BaseAPIConfig):
    URL: str = Field(..., alias="NUMBERS_URL")


class CatsNinjaAPIConfig(BaseAPIConfig):
    URL: str = Field(..., alias="CATS_NINJA_URL")


class UselessFactsAPIConfig(BaseAPIConfig):
    URL: str = Field(..., alias="USELESS_FACTS_URL")


class MeowFactsAPIConfig(BaseAPIConfig):
    URL: str = Field(..., alias="MEOW_FACTS_URL")


# Jokes
class RandomJokeAPIConfig(BaseAPIConfig):
    URL: str = Field(..., alias="RANDOM_JOKE_URL")


class DadJokeAPIConfig(BaseAPIConfig):
    URL: str = Field(..., alias="DAD_JOKE_URL")


class ChuckNorrisAPIConfig(BaseAPIConfig):
    URL: str = Field(..., alias="CHUCK_NORRIS_URL")


# Quizzes
class OpenTdbAPIConfig(BaseAPIConfig):
    URL: str = Field(..., alias="OPEN_TDB_URL")

