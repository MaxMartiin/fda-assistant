import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

load_dotenv()
# pool_pre_ping: Neon sleeps when idle; this checks the connection before each use
engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class RequestLog(Base):
    __tablename__ = "request_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    model: Mapped[str] = mapped_column(String(64))
    prompt_chars: Mapped[int]
    cache_write_tokens: Mapped[int] = mapped_column(default=0)
    cache_read_tokens: Mapped[int] = mapped_column(default=0)
    input_tokens: Mapped[int]
    output_tokens: Mapped[int]
    ttft_s: Mapped[float | None]
    total_s: Mapped[float]
    cost_usd: Mapped[float]
    stop_reason: Mapped[str | None] = mapped_column(String(64))


Base.metadata.create_all(engine)  # creates the table if it doesn't exist


def save_log(**fields) -> None:
    with Session(engine) as session:
        session.add(RequestLog(**fields))
        session.commit()
