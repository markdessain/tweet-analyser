import logging

from utils.redis import Object, SortedSet
from utils.string import random_string

log = logging.getLogger(__name__)


class Query(Object):
    singular = 'query'
    plural = 'queries'

    def __init__(self, _id: object=None) -> None:
        _id = _id or random_string()
        super(Query, self).__init__(_id)

    def save(self, **kwargs: dict) -> None:
        super(Query, self).save(kwargs)

    def add_results(self, name: str, results: list) -> None:
        query_results = QueryResults(self.id, name)
        for result in results:
            query_results.increment(result)

    def load_results(self, name) -> list:
        query_results = QueryResults(self.id, name)
        return query_results.all()


class QueryResults(SortedSet):
    singular = 'query'
    plural = 'queries'

    def __init__(self, _id: object, name: str) -> None:
        super(QueryResults, self).__init__([_id, name])


class Tweet(Object):
    singular = 'tweet'
    plural = 'tweets'

    @property
    def text(self) -> str:
        return self.load().get('text')

    @property
    def media_url(self) -> str:
        try:
            size = 'thumb'
            return '%s:%s' % (self.load().get('entities').get('media')[0].get('media_url'), size)
        except:
            return None
