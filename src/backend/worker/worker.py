import time
from backend.database.session import Database
from backend.services.secret import Settings


class Worker:
    def __init__(self, settings: Settings):
        self.db = Database(settings)

    def run(self):
        while True:
            jobs = self.db.get_due_jobs()
            for job in jobs:
                print(job)
                self.db.update_timing(job.id)
                # update next_run_at column with time + interval

            time.sleep(1)


if __name__ == "__main__":
    w = Worker(Settings())
    w.run()
