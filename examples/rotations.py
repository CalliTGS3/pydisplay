"""
rotations.py
============

.. figure:: ../_static/rotations.jpg
    :align: center

    Test for rotations and colors.

Rotates the display 0, 90, 180, and 270 degrees and displays the rotation
number and the color of the display background.

.. note:: This example requires the following modules:

  .. hlist::
    :columns: 3

    - `st7789py`
    - `tft_config`
    - vga1_16x16

"""

import time
import tft_config

pallette = tft_config.Pallette
import vga1_16x16 as font


def center_on(display, using_font, text, y, fg, bg):
    """
    Center the text on the display
    """
    x = (display.width - len(text) * font.WIDTH) // 2
    display.text(using_font, text, x, y, fg, bg)


def clear_screen(display, color):
    """
    Clear the screen by drawing rectangles starting from the center of the display
    and working towards the edges.

    Args:
        display: The display object to clear.
    """
    width = display.width
    height = display.height
    x_center = width // 2
    y_center = height // 2

    for i in range(min(x_center, y_center)):
        x = x_center - i
        y = y_center - i
        rect_width = 2 * i + 1
        rect_height = 2 * i + 1
        display.rect(x, y, rect_width, rect_height, color)


def main():
    """
    The big show!
    """
    # enable display and clear screen

    tft = tft_config.config(tft_config.WIDE)

    colors = (
        ("Red", pallette.RED, pallette.WHITE),
        ("Green", pallette.GREEN, pallette.BLACK),
        ("Blue", pallette.BLUE, pallette.WHITE),
        ("Black", pallette.BLACK, pallette.WHITE),
        ("White", pallette.WHITE, pallette.BLACK),
        ("Yellow", pallette.YELLOW, pallette.BLACK),
        ("Cyan", pallette.CYAN, pallette.BLACK),
        ("Magenta", pallette.MAGENTA, pallette.BLACK),
    )

    color_idx = 0
    while True:
        for rotation in range(4):
            tft.rotation = rotation
            height = tft.height
            width = tft.width
            fg = colors[color_idx][2]
            bg = colors[color_idx][1]

            tft.fill(bg)

            tft.rect(0, 0, width, height, pallette.WHITE)
            center_on(tft, font, "Rotation", height // 3 - font.HEIGHT // 2, fg, bg)
            center_on(tft, font, str(rotation), height // 2 - font.HEIGHT // 2, fg, bg)
            center_on(
                tft,
                font,
                colors[color_idx][0],
                height // 3 * 2 - font.HEIGHT // 2,
                fg,
                bg,
            )
            color_idx = (color_idx + 1) % len(colors)
            time.sleep(2)


main()
