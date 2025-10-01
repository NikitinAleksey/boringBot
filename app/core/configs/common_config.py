from pydantic import Field
from pydantic_settings import BaseSettings


class CommonConfig(BaseSettings):
    # Common api error message
    API_ERROR: str = Field(..., alias="API_ERROR")
