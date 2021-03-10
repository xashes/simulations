#!/usr/bin/env python3

import numpy as np
import pyglet


class Walker:
    def __init__(self, position: list[float]):
        self.position = np.array(position)

    def display(self):
        x, y = self.position
        circle = pyglet.shapes.Circle(x, y, radius=20, color=(50, 255, 30))
        circle.draw()


window = pyglet.window.Window()

pos = [window.width // 2, window.height // 2]
walker = Walker(pos)


@window.event
def on_draw():
    walker.display()


if __name__ == "__main__":
    pyglet.app.run()
