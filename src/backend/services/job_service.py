from datetime import datetime, timedelta

from marktplaats import SearchQuery, category_from_name

from backend.api.schemas.jobs import SearchJobCreate
from backend.api.schemas.users import UserCreate, UserResponse
from backend.database.models import Job, User


class JobService:
    def __init__(self, db):
        self.db = db

    def create_user(self, user: UserCreate):
        return self.db.create_user(user)

    def create_job(self, job: SearchJobCreate) -> Job:
        user = self.db.get_user_by_token(job.token)
        params = job.model_dump(
            mode="json",
            exclude_none=True,
            exclude={"check_interval"},
        )

        current_time = datetime.now()

        db_job = Job(
            user_id=user.id,
            check_interval=job.check_interval,
            params=params,
            last_run_at=current_time,
            next_run_at=current_time + timedelta(seconds=job.check_interval),
        )

        return self.db.submit_job(db_job)


def build_search_query(job) -> SearchQuery:
    category = category_from_name(job.category_name) if job.category_name else None

    try:
        query = SearchQuery(
            query=job.query,
            zip_code=job.zip_code or "",
            distance=job.distance or 1_000_000,
            price_from=job.price_from,
            price_to=job.price_to,
            limit=job.limit,
            offset=job.offset,
            sort_by=job.sort_by,
            sort_order=job.sort_order,
            condition=job.condition,
            offered_since=job.offered_since,
            category=category,
            extra_attributes=job.extra_attributes,
        )
    except KeyError as e:
        print(e)
