import mock

from models import Query, Tweet
from streams.twitter import load_tweets, aggregate_adjectives


class TweetResult(object):
    def __init__(self, _id):
        self.id = _id
        self.id_str = _id
        self._json = {'id': _id}


def test_load_tweet_loads_the_correct_number_of_pages():
    with mock.patch('tweepy.API') as mock_tweepy:
        mock_tweepy.return_value.search.return_value = [TweetResult(1), TweetResult(2), TweetResult(3)]
        tweets = list(load_tweets(9, 'test'))
        assert len(tweets) == 9


# def test_aggregate_adjectives():
#
#     tweet = {'text': 'testing tweet'}
#
#     mock_query = mock.Mock()
#     mock_query.load_results.return_value = [1, 2, 3]
#
#     with mock.patch.object(Tweet, 'load', return_value=tweet):
#         a = aggregate_adjectives(mock_query)
#
#         assert len(list(a)) == 1
#
