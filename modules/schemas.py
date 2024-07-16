from pydantic import BaseModel


class DownloadList(BaseModel):
    available_downloads: list[str]
