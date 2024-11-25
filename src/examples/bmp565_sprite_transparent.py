# from board_config import display_drv as canvas
from color_setup import ssd as canvas
from bmp565 import BMP565
from time import sleep
from random import choice
from collections import namedtuple


show = canvas.show if hasattr(canvas, "show") else lambda _: None


image = BMP565("examples/assets/warrior.bmp", streamed=True)
print(f"\n{image.width=}, {image.height=}, {image.bpp=}")
sprite_height = image.height // 4
sprite_width = image.width // 3
transparent = image[0]  # top left pixel is the background color
bg = -1  # white background
print(f"{sprite_width=}, {sprite_height=} {bg=:#0x}\n")


back, right, fwd, left = [x * sprite_height for x in range(4)]
directions = [fwd, left, right, back]
a, b, c = [x * sprite_width for x in range(3)]
positions = [a, b, c, b]
pos_per_step = len(positions)
print("Sprite coordinates:")
for col in [fwd, left, right, back]:
    print(f"{(a, col)} {(b, col)} {(c, col)} {(b, col)}")


def draw_sprite(
    dest_x,
    dest_y,
    source_x,
    source_y,
    source_image=image,
    width=sprite_width,
    height=sprite_height,
):
    return canvas.blit_transparent(
        source_image[source_x : source_x + width, source_y : source_y + height],
        dest_x,
        dest_y,
        width,
        height,
        transparent,
    )


canvas.fill(bg)
show()

point = namedtuple("point", "x y")
location = point(0, 0)
sprite = (a, fwd)
draw_sprite(*location, *sprite)

step = 3
dir = choice(directions)
while True:
    if choice((True, False, False, False, False)):  # 20% chance of changing direction
        dir = choice(directions)
    if dir == fwd and location.y + sprite_height > canvas.height - step * pos_per_step:
        continue
    elif dir == back and location.y < step * pos_per_step:
        continue
    elif dir == left and location.x < step * pos_per_step:
        continue
    elif dir == right and location.x + sprite_width > canvas.width - step * pos_per_step:
        continue

    for pos in positions:
        dirty = canvas.fill_rect(location.x, location.y, sprite_width, sprite_height, bg)
        if dir == fwd:
            location = point(location.x, location.y + step)
        elif dir == back:
            location = point(location.x, location.y - step)
        elif dir == left:
            location = point(location.x - step, location.y)
        elif dir == right:
            location = point(location.x + step, location.y)
        dirty += draw_sprite(*location, pos, dir)
        show(dirty)
        sleep(0.1)
