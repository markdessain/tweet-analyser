import json
import logging

from settings import redis_db

log = logging.getLogger(__name__)


class Storage(object):
    singular = ''
    plural = ''

    def __init__(self, _id: object) -> None:
        if isinstance(_id, list):
            _id = ':'.join(_id)
        self.id = _id

    def path(self) -> str:
        return '%s:%s' % (self.singular, self.id)


class Object(Storage):
    def load(self) -> dict:
        data = redis_db.get(self.path())
        return json.loads(data.decode('utf8'))

    def save(self, data: object) -> None:
        redis_db.set(self.path(), json.dumps(data))

    @classmethod
    def keys(cls) -> list:
        return redis_db.keys('%s:*' % cls.singular)


class Set(Storage):
    def add(self, data: object) -> None:
        redis_db.sadd(self.path(), data)


class List(Storage):
    def add(self, data: object) -> None:
        redis_db.rpush(self.path(), data)

    def all(self) -> list:
        return [data.decode('utf8') for data in redis_db.lrange(self.path(), 0, -1)]


class SortedSet(Storage):
    def increment(self, data: object, score: int=1) -> None:
        redis_db.zincrby(self.path(), data, score)

    def all(self) -> list:
        data = redis_db.zrange(self.path(), 0, -1)
        return [x.decode('utf8').replace("'", '"') for x in data]
