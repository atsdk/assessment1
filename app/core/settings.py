import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Lets say, for the ease of this example, that we have a
    # static token that we use for authentication
    auth_token: str
    data_dir: str = "data"
    file_chunk_size: int = 1024 * 1024  # 1 MB
    max_file_size: int = 1024 * 1024 * 100  # 500 MB
    max_single_read_file_size: int = 1024 * 1024 * 250  # 250 MB
    max_filename_length: int = 255
    app_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root_dir: str = os.path.dirname(app_dir)
    # And also for the ease of use we use the same settings obj for everything
    database_uri: str


# TODO: Add logging configuration


settings = Settings()
