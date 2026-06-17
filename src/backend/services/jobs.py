from marktplaats import SearchQuery, category_from_name

from backend.api.schemas.jobs import SearchJobBase


def build_search_query(job: SearchJobBase) -> SearchQuery:
    category = category_from_name(job.category_name) if job.category_name else None

    return SearchQuery(
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