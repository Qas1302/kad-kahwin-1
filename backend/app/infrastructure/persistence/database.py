from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool


class Base(DeclarativeBase):
    pass


def _normalise_url(raw: str) -> URL:
    """Accept the plain postgres:// URLs Supabase shows and use the psycopg 3 driver."""
    url = make_url(raw)
    if url.drivername in ("postgres", "postgresql"):
        url = url.set(drivername="postgresql+psycopg")
    return url


class Database:
    def __init__(self, raw_url: str) -> None:
        url = _normalise_url(raw_url)
        options: dict[str, object] = {}

        if url.get_backend_name() == "sqlite":
            options["connect_args"] = {"check_same_thread": False}
            if url.database and url.database != ":memory:":
                Path(url.database).parent.mkdir(parents=True, exist_ok=True)
        elif url.get_backend_name() == "postgresql":
            # Serverless friendly: let the Supabase pooler (Supavisor) do the pooling,
            # and skip prepared statements, which its transaction mode doesn't support.
            options["poolclass"] = NullPool
            options["connect_args"] = {"prepare_threshold": None}

        self.engine: Engine = create_engine(url, **options)
        self._sessions = sessionmaker(bind=self.engine, expire_on_commit=False)

    def create_schema(self) -> None:
        # Imported for its side effect of registering the tables on Base.metadata.
        from app.infrastructure.persistence import models  # noqa: F401

        Base.metadata.create_all(self.engine)

    def session(self) -> Iterator[Session]:
        with self._sessions() as session:
            yield session
