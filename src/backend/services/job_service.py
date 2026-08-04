from datetime import datetime, timedelta, UTC

from marktplaats import SearchQuery, category_from_name, SortBy, SortOrder, Condition

from backend.api.schemas.jobs import SearchJobCreate, SearchParams
from backend.api.schemas.users import UserCreate, UserResponse
from backend.database.models import Job, User


class JobService:
    def __init__(self, db):
        self.db = db

    def create_user(self, user: UserCreate):
        return self.db.create_user(user)

    def create_job(self, job: SearchJobCreate) -> Job:
        user = self.db.get_user_by_token(job.token)
        params = job.search.model_dump(
            mode="json",
            exclude_none=True,
        )

        db_job = Job(
            user_id=user.id,
            check_interval=job.check_interval,
            params=params,
            enabled=True,
            last_run_at=datetime.now(UTC),
        )

        return self.db.submit_job(db_job)

def build_search_query(
    params: SearchParams,
    offered_since,
) -> SearchQuery:
    category = (
        category_from_name(params.category_name)
        if params.category_name
        else None
    )

    condition = (
        Condition[params.condition]
        if params.condition is not None
        else None
    )

    return SearchQuery(
        query=params.query,
        zip_code=params.zip_code or "",
        distance_km=params.distance_km,
        price_from=params.price_from,
        price_to=params.price_to,
        limit=10,
        offset=0,
        sort_by=SortBy.DATE,
        sort_order=SortOrder.DESC,
        condition=condition,
        offered_since=offered_since,
        category=category,
        extra_attributes=params.extra_attributes,
    )
