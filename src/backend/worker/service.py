import logging
import time

from backend.api.schemas.jobs import SearchParams
from backend.api.schemas.notifiers import NtfyNotifierParams
from backend.database.models import Job
from backend.database.session import Database
from backend.notifications.service import compose_message, create_notifier
from backend.services.job_service import build_search_query
from backend.services.secret import Settings


logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, settings: Settings):
        self.db = Database(settings)


    def process_job(self, job: Job) -> None:
        params = SearchParams.model_validate(job.params)

        search_query = build_search_query(
            params=params,
            offered_since=job.last_run_at,
        )

        listings = list(search_query.get_listings())
        print(f"Found {len(listings)} listings for Job ID: {job.id}")

        if listings:
            notifier = create_notifier(
                NtfyNotifierParams.model_validate(job.user.notifier_params)
            )

            notifier.send(compose_message(listings))

        self.db.update_last_run(job.id)

    def run_once(self) -> None:
        jobs: list[Job] = self.db.get_due_jobs()

        logger.info("Found %s due jobs", len(jobs))

        for job in jobs:
            try:
                self.process_job(job)
            except Exception:
                logger.exception(
                    "Job %s failed",
                    job.id,
                )

    def run(self) -> None:
        logger.info("Worker started")

        while True:
            self.run_once()
            time.sleep(1)