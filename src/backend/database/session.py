# src/backend/database/session.py
from datetime import datetime, UTC, timedelta

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

from backend.database.models import Base, Job, User


class Settings(BaseSettings):
    db_host: str
    db_user: str
    db_password: str
    db_name: str

    class Config:
        env_file = ".env"


class Database:
    def __init__(self):
        settings = Settings()

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

    def get_or_create_user_by_email(self, email: str):
        with self.session() as session:
            user = session.scalar(select(User).where(User.email == email))

            if user is None:
                user = User(email=email)
                session.add(user)
                session.commit()
                session.refresh(user)

            return user

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
