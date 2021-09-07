from dataclasses import dataclass
from random import randint

import pyxel

from transiri import tween


@dataclass
class Circle:
    x: float
    y: float
    radius: float
    colour: int


circles: list[Circle] = []


def update():
    if pyxel.btnp(pyxel.KEY_SPACE):
        c = Circle(
            x=randint(10, 240),
            y=randint(10, 240),
            radius=randint(1, 10),
            colour=randint(1, 15),
        )
        circles.append(c)
        duration = randint(1, 5)
        tween.start(c, "x", start_value=c.x, end_value=randint(10, 240), duration=duration)
        tween.start(c, "y", start_value=c.y, end_value=randint(10, 240), duration=duration)
        tween.start(
            c,
            "radius",
            start_value=c.radius,
            end_value=randint(1, 10),
            duration=duration,
            on_complete=lambda x: circles.remove(x),
        )
    tween.update()


def draw():
    pyxel.cls(0)

    for circle in circles:
        pyxel.circ(circle.x, circle.y, circle.radius, circle.colour)


pyxel.init(250, 250, caption="tweening prototype")
pyxel.run(update, draw)
