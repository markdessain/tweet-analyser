import os
import logging

import redis


def get_env() -> dict:
    if not os.environ.get('ENV'):
        a = os.path.join(os.path.dirname(__file__), '../environment/test')
        with open(a) as f:
            defaults = dict(tuple(x.strip().split('=')) for x in f.readlines() if x != '\n')
        return defaults
    else:
        return os.environ


env = get_env()

logging.basicConfig(level=getattr(logging, env.get('LOG_LEVEL').upper()))

redis_db = redis.Redis(env.get('REDIS_HOST'), port=int(env.get('REDIS_PORT')))

twitter_access_token = env.get('TWITTER_ACCESS_TOKEN')
twitter_access_secret = env.get('TWITTER_ACCESS_SECRET')
twitter_consumer_key = env.get('TWITTER_CONSUMER_KEY')
twitter_consumer_secret = env.get('TWITTER_CONSUMER_SECRET')
