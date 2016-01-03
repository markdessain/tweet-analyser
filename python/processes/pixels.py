import math
import logging
from typing import Generator

import requests
from PIL import Image
from io import BytesIO

from processes.kmeans import Kmeans

log = logging.getLogger(__name__)


def get_image(media_url: str) -> Image:
    response = requests.get(media_url)
    filename = BytesIO(response.content)
    return Image.open(filename)


def run(media_url: str, k: int=10) -> Generator:
    try:
        k = Kmeans(k, max_iterations=1, size=10)
        image = get_image(media_url)
        result = k.run(image)
        log.info(result)

        for rgb in result:
            rgb = list(map(math.floor, rgb))
            yield rgb
    except Exception:
        log.error('Unable to process images: %s', media_url)
