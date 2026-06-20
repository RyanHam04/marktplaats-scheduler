# src/backend/database/models.py
from datetime import datetime

from narwhals import Boolean
from sqlalchemy import ForeignKey, String, BigInteger, Text, UniqueConstraint
from sqlalchemy.dialects.mssql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    jobs: Mapped[list["Job"]] = relationship(back_populates="user")


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    check_interval: Mapped[int] = mapped_column(BigInteger, nullable=False)
    params: Mapped[dict] = mapped_column(JSON, nullable=False)

    user: Mapped["User"] = relationship(back_populates="jobs")
    last_seen_ads: Mapped[list["LastSeenAd"]] = relationship(back_populates="job")
    enabled: Mapped[bool] = mapped_column(default=True)

    next_run_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    last_run_at: Mapped[datetime] = mapped_column(nullable=False)


class LastSeenAd(Base):
    __tablename__ = "last_seen_ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    marktplaats_id: Mapped[str] = mapped_column(Text, nullable=False)

    job: Mapped["Job"] = relationship(back_populates="last_seen_ads")

    __table_args__ = (UniqueConstraint("job_id", "marktplaats_id"),)


class Subscriptions(Base):
    __tablename__ = "push_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    subscription: Mapped[dict] = mapped_column(JSON, nullable=False)
