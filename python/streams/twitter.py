import logging
from typing import Generator

import tweepy
from rq import Queue

import settings
from models import Tweet, Query
from processes import adjectives, pixels

log = logging.getLogger(__name__)


def search(input: str, size: int=100) -> Query:
    """Adds search query into a queue for importing and processing
    """
    # TODO - Take into account the rate limit, the importer will fail and need adding back to the queue if hit
    # TODO - multi depends_on maybe coming soon. It would allow a end of processing notification to exist

    query = Query()
    query.save(input=input, size=size, stream='twitter')

    source_queue = Queue(name='source')
    process_queue = Queue(name='process')

    # Import tweets
    import_job = source_queue.enqueue(import_raw, query=query)

    # Process tweets
    process_queue.enqueue(aggregate_pixels, query=query, depends_on=import_job)
    process_queue.enqueue(aggregate_adjectives, query=query, depends_on=import_job)

    return query


def import_raw(query: Query) -> None:
    """Queries twitter based on the query, stores the raw results
    """
    parameters = query.load()

    results = load_tweets(parameters.get('size'), parameters.get('input'))
    ids = save_raw(results)

    query.add_results('tweet', ids)


def load_tweets(max_tweets: int, q: str) -> Generator:
    """Searches twitter and generates the max_tweet results that may span multiple api calls
    """
    auth = tweepy.OAuthHandler(settings.twitter_consumer_key, settings.twitter_consumer_secret)
    auth.set_access_token(settings.twitter_access_token, settings.twitter_access_secret)

    api = tweepy.API(auth)

    len_result = 0
    last_id = -1
    while len_result < max_tweets:
        count = max_tweets - len_result
        try:
            new_tweets = api.search(q=q, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break

            for tweet in new_tweets:
                yield tweet

            len_result += len(new_tweets)

            last_id = new_tweets[-1].id
        except tweepy.TweepError:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break


def save_raw(results: Generator) -> Generator:
    """Save the results and yields the id values
    """
    for result in results:
        id_str = result.__dict__.get('id_str')
        data = result.__dict__.get('_json')

        tweet = Tweet(id_str)
        tweet.save(data)

        yield id_str


def aggregate_pixels(query) -> None:
    tweet_ids = query.load_results('tweet')
    for tweet_id in tweet_ids:
        t = Tweet(tweet_id)
        query.add_results('pixels', pixels.run(t.media_url))


def aggregate_adjectives(query) -> None:
    tweet_ids = query.load_results('tweet')
    for tweet_id in tweet_ids:
        t = Tweet(tweet_id)
        query.add_results('adjectives', adjectives.run(t.text))
