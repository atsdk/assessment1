from pydantic import BaseSettings


class Settings(BaseSettings):
    # Lets say, for the ease of this example, that we have a
    # static token that we use for authentication
    AUTH_TOKEN: str


settings = Settings()
