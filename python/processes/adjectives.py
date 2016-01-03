import os
import re
import string
import logging
from typing import Generator

log = logging.getLogger(__name__)


def get_adjectives() -> set:
    a = os.path.join(os.path.dirname(__file__), '../../data/adjectives.txt')
    with open(a) as f:
        return set(sum([x[:-1].split() for x in f.readlines()], []))


def run(text: str) -> Generator:
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    adjectives = get_adjectives()
    words = regex.sub('', text).split()

    for word in words:
        if word.lower() in adjectives:
            yield word.lower()
