import logging

from backend.services.secret import Settings
from backend.worker.service import Worker


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    Worker(Settings()).run()


if __name__ == "__main__":
    main()