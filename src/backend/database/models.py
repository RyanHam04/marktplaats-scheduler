# src/backend/database/models.py
from datetime import datetime


from sqlalchemy import ForeignKey, String, BigInteger, Text, UniqueConstraint, DateTime
from sqlalchemy.dialects.mssql import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    notifier_params: Mapped[dict] = mapped_column(JSON, nullable=False)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)

    jobs: Mapped[list["Job"]] = relationship(back_populates="user")


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    check_interval: Mapped[int] = mapped_column(BigInteger, nullable=False)
    params: Mapped[dict] = mapped_column(JSON, nullable=False)

    user: Mapped["User"] = relationship(back_populates="jobs")
    enabled: Mapped[bool] = mapped_column(default=True)

    last_run_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True, index=True)



# class Notifier(Base):
#    params: Mapped[dict] = mapped_column(JSON, nullable=False)
