import logging
import time

import dramatiq


@dramatiq.actor()
def process_user_stats():
    """Very simple task for demonstrating purpose."""
    logging.warning('Start my long-running task')
    time.sleep(5)
    logging.warning('Task is ended')
