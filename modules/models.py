# from datetime import datetime

from sqlalchemy.orm import Mapped, registry, mapped_column

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    # created_at: Mapped[datetime]


@table_registry.mapped_as_dataclass
class ScrapeTarget:
    __tablename__ = 'scrape_target'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    target: Mapped[str]
    url: Mapped[str]
    # created_at: Mapped[datetime]
