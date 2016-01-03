
from nose import with_setup
from rq import SimpleWorker, Connection, Queue

from streams import twitter
from settings import redis_db
from models import Tweet, Query


def setup_func():
    redis_db.flushdb()


@with_setup(setup_func)
def test_twitter_search_gets_added_onto_queue_to_be_processed():
    """Ensures that multiple queries get added onto an empty queue

    Run four search queries
    Check size of queries added in four
    Check size of queue is four
    """

    with Connection(connection=redis_db):
        queue = Queue(name='source')

        query = 'Test Query'
        twitter.search(input=query)
        twitter.search(input=query)
        twitter.search(input=query)
        twitter.search(input=query)

        assert len(Query.keys()) == 4
        assert queue.count == 4


@with_setup(setup_func)
def test_twitter_search_gets_processed():
    """Ensures the data can be loaded from twitter and stored as a raw source

    Run one search query
    Run worker
    Check two tweets in raw source
    Run worker
    Check the pixels have been averaged out
    """

    with Connection(connection=redis_db):
        source_queue = Queue(name='source')
        process_queue = Queue(name='process')

        query = 'Test Query'
        size = 2
        twitter.search(input=query, size=size)

        worker = SimpleWorker([source_queue])
        worker.work(burst=True)

        assert len(Tweet.keys()) == size

        worker = SimpleWorker([process_queue])
        worker.work(burst=True)
        #
        # assert len(Tweet.keys()) == size