# src/backend/database/session.py
from datetime import datetime, UTC, timedelta

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import secrets
from backend.api.schemas.users import UserCreate
from backend.database.models import Base, Job, User
from backend.services.secret import Settings


class Database:
    def __init__(self, settings: Settings):
        db_url = (
            f"postgresql+psycopg://{settings.db_user}:"
            f"{settings.db_password}@{settings.db_host}/{settings.db_name}"
        )
        self.engine = create_engine(db_url)
        self.session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def submit_job(self, job):
        with self.session() as session:
            session.add(job)
            session.commit()
            session.refresh(job)
            return job

    def delete_job(self, job_id):
        with self.session() as session:
            session.query(Job).filter(Job.id == job_id).delete()
            session.commit()

    def get_user_by_token(self, token: str):
        with self.session() as session:
            user_db = session.scalar(select(User).where(User.token == token))
            print(token)
            if user_db is None:
                raise ValueError("Invalid user token")

            return user_db

    def create_user(self, user: UserCreate):
        with self.session() as session:
            user_db = session.scalar(select(User).where(User.email == user.email))

            if user_db is not None:
                raise ValueError("User already exists")

            user_db = User(
                email=user.email,
                token=secrets.token_urlsafe(32),
                notifier_params=user.notifier_params.model_dump(mode="json"),
            )

            session.add(user_db)
            session.commit()
            session.refresh(user_db)

            return user_db

    def get_due_jobs(self):
        with self.session() as session:
            print(datetime.now())
            return list(
                session.scalars(select(Job).where(Job.next_run_at <= datetime.now()))
            )

    def update_timing(self, job_id):
        with self.session() as session:
            job = session.scalar(select(Job).where(Job.id == job_id))

            if job is None:
                raise ValueError(f"Job {job_id} not found")

            now = datetime.now()

            job.last_run_at = now
            job.next_run_at = now + timedelta(seconds=job.check_interval)
            session.commit()


if __name__ == "__main__":
    db = Database()
    db.drop_tables()
    db.create_tables()
