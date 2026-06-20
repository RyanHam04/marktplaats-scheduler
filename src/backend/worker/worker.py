import time
from backend.database.session import Database


class Worker:
    def __init__(self):
        self.db = Database()

    def run(self):
        while True:
            jobs = self.db.get_due_jobs()
            for job in jobs:
                print(job.id)
                self.db.update_timing(job.id)
                # update next_run_at column with time + interval

            time.sleep(1)


if __name__ == "__main__":
    w = Worker()
    w.run()
