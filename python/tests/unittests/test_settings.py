import settings


def test_redis_db():
    assert settings.redis_db


def test_env():
    assert isinstance(settings.env, dict)