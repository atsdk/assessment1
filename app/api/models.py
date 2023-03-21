from pydantic import BaseModel


class ErrorBase(BaseModel):
    error: str


class FileResponseBase(BaseModel):
    filename: str
    message: str
