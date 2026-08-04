# src/backend/database/session.py
from datetime import datetime, timedelta, UTC

from sqlalchemy import create_engine, select, URL
from sqlalchemy.orm import sessionmaker, selectinload
import secrets
from backend.api.schemas.users import UserCreate
from backend.database.models import Base, Job, User
from backend.services.secret import Settings


class Database:
    def __init__(self, settings: Settings):
        db_url = URL.create(
            drivername="postgresql+psycopg",
            username=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
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
            job = session.scalar(select(Job).where(Job.id == job_id))
            if job is None:
                raise ValueError(f"Job {job_id} not found")

            session.delete(job)

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
            user_db = User(
                token=secrets.token_urlsafe(32),
                notifier_params=user.notifier_params.model_dump(
                    mode="json",
                ),
            )

            session.add(user_db)
            session.commit()
            session.refresh(user_db)

            return user_db

    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    def get_due_jobs(self) -> list[Job]:
        now = datetime.now(UTC)

        with self.session() as session:
            jobs = list(
                session.scalars(
                    select(Job)
                    .options(selectinload(Job.user))
                    .where(Job.enabled.is_(True))
                    .order_by(Job.id)
                )
            )

            return [
                job
                for job in jobs
                if job.last_run_at is None
                   or (
                           now - job.last_run_at
                   ).total_seconds() >= job.check_interval
            ]

    def update_last_run(self, job_id):
        with self.session() as session:
            job = session.scalar(select(Job).where(Job.id == job_id))

            if job is None:
                raise ValueError(f"Job {job_id} not found")

            job.last_run_at = datetime.now(UTC)
            session.commit()
