import time
import logging

from rq import Connection

from streams import twitter
from settings import redis_db

log = logging.getLogger(__name__)


# TODO - A web interface would submit queries to the workers
# TODO - Use Flask to create a simple search box for submitting queries and viewing results

if __name__ == "__main__":

    time.sleep(4)

    redis_db.flushdb()

    with Connection(connection=redis_db):
        twitter.search('New Year')
        twitter.search('New Year filter:images')
        twitter.search('Mark')

    while True:
        time.sleep(10)
