from marktplaats import SearchQuery, category_from_name

from backend.api.schemas.jobs import SearchJobCreate
from backend.api.schemas.users import UserRequest, UserResponse
from backend.database.models import Job


class JobService:
    def __init__(self, db):
        self.db = db


    def create_user(self, user: UserRequest):
        return self.db.get_or_create_user_by_email(user.email)

    def create_job(self, job: SearchJobCreate) -> Job:
        user = self.db.get_or_create_user_by_email(job.email)
        params = job.model_dump(mode='json', exclude_none=True, exclude={'email', 'check_interval'})
        db_job = Job(
            user_id=user.id,
            check_interval=job.check_interval,
            params=params,
        )
        self.db.submit_job(db_job)
        return db_job



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

