import mock

from PIL import Image, ImageDraw

from processes.pixels import run


def draw_image():
    white = (255, 255, 255)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0,128,0)

    width = 10
    height = 10

    image = Image.new("RGB", (width, height), white)
    draw = ImageDraw.Draw(image)

    draw.line((0, 0, 0, 1), red, 1)
    draw.line((5, 0, 5, 3), green, 1)
    draw.line((9, 5, 9, 9), blue, 1)

    return image


def test_run_with_a_small_image():
    with mock.patch('processes.pixels.get_image', return_value=draw_image()):
        assert len(list(run('mock', k=1))) == 1
