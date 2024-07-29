from pydantic import BaseModel


class DownloadList(BaseModel):
    available_downloads: list[str]


class UserInfo(BaseModel):
    user: str
    password: str
    email: str
