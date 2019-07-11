import random
from collections import namedtuple

import numpy as np
import PIL.Image
import PIL.ImageColor


FILLED = 1
EMPTY = 0
BLACK = PIL.ImageColor.getcolor("black", "RGBA")
INITIAL_CHANCE = 0.4
IMAGE_FILE_NAME = "test_maps/test_map"

Point = namedtuple("Point", ["x", "y"])


class CaveGenerator:
    cave_map: np.array
    map_height: int
    map_width: int

    def in_bounds(self, point: Point) -> bool:
        return 0 <= point.x < self.map_width and 0 <= point.y < self.map_height

    @property
    def height(self) -> int:
        return self.map_height

    @height.setter
    def height(self, value: int):
        self.map_height = value

    @property
    def width(self) -> int:
        return self.map_width

    @width.setter
    def width(self, value: int):
        self.map_width = value

    def find_one_step_neighbors(self, center: Point) -> int:
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                point = Point(x=center.x + j, y=center.y + i)
                if not self.in_bounds(point=point):
                    continue
                if self.cave_map[point.x, point.y] == FILLED:
                    count += 1

        return count

    def find_two_step_neighbors(self, center: Point) -> int:
        count = 0
        for i in range(-2, 2):
            for j in range(-2, 2):
                if abs(i) == 2 and abs(j) == 2:
                    continue

                point = Point(x=center.x + j, y=center.y + i)
                if not self.in_bounds(point):
                    continue
                if self.cave_map[point.x, point.y] == FILLED:
                    count += 1

        return count

    def smooth_step(self, min_count: int, max_count: int):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                point = Point(x=j, y=i)
                count1 = self.find_one_step_neighbors(center=point)
                count2 = self.find_two_step_neighbors(center=point)

                if count1 >= min_count:
                    self.cave_map[point.x, point.y] = FILLED
                elif count2 <= max_count:
                    self.cave_map[point.x, point.y] = FILLED
                else:
                    self.cave_map[point.x, point.y] = EMPTY

    def map_to_image(self, suffix: str = None):
        image = PIL.Image.new("RGBA", (self.width, self.height), "white")

        for i in range(self.height):
            for j in range(self.width):
                if self.cave_map[j, i] == FILLED:
                    image.putpixel((j, i), BLACK)

        file_name = IMAGE_FILE_NAME
        if suffix:
            file_name += suffix
        image.save(file_name + ".png")

    def reset_map(self):
        new_map = np.zeros((self.height, self.width), order="F")
        self.cave_map = new_map

    def initialize_map(self):
        new_map = np.zeros((self.width, self.height), order="F")

        for i in range(self.height):
            for j in range(self.width):
                if i == 0 or j == 0 or i == self.height - 1 or j == self.map_width - 1:
                    new_map[j, i] = FILLED

                if random.random() < INITIAL_CHANCE:
                    new_map[j, i] = FILLED

        self.cave_map = new_map

    def create_new_map(self):
        self.initialize_map()
