"""
font_simpletest.py -- Simple test of the Font class.
inspired by Russ Hughes's hello.py

Draws to a DisplayBuffer and only updates the area that has changed.
"""

from board_config import display_drv
from graphics import Font
import random
from displaybuf import DisplayBuffer
from palettes import get_palette


display = DisplayBuffer(display_drv)

BPP = display.color_depth // 8  # Bytes per pixel

def write(font, string, x, y, fg_color, bg_color, scale):
    """
    Write text to the display.
    """
    dirty = font.text(display, string, x, y, fg_color, scale)
    display.show(dirty)


def main():
    """
    The big show!
    """
    pal = get_palette()

    write_text = "Hello!"
    text_len = len(write_text)
    iterations = 32

    directory = "examples/assets/"
    font1 = Font(f"{directory}font_8x8.bin")
    font2 = Font(f"{directory}font_8x14.bin")
    font3 = Font(f"{directory}font_8x16.bin")
    fonts = [font1, font2, font3]

    max_width = max([font.width for font in fonts])
    max_height = max([font.height for font in fonts])

    while True:
        for rotation in range(4):
            scale = rotation + 1
            display.rotation = rotation * 90
            width, height = display.width, display.height
            # display.fill_rect(0, 0, width, height, 0x0000)

            col_max = width - max_width * scale * text_len
            row_max = height - max_height * scale
            if col_max < 0 or row_max < 0:
                raise RuntimeError("This font is too big to display on this screen.")

            for _ in range(iterations):
                write(
                    fonts[random.randint(0, len(fonts) - 1)],
                    write_text,
                    random.randint(0, col_max),
                    random.randint(0, row_max),
                    pal[random.randint(0, len(pal) - 1)],
                    pal[random.randint(0, len(pal) - 1)],
                    scale,
                )


main()
