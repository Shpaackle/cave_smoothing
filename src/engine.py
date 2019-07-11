import random
from typing import Optional

from kivy import app as kv_app
from kivy.uix import boxlayout as kv_box_layout
from kivy.uix import image as kv_image
from kivy.properties import ObjectProperty

from cave_generator import CaveGenerator


class MapGenerator(kv_box_layout.BoxLayout):
    map_image: ObjectProperty()
    map_width_input: ObjectProperty()
    map_height_input: ObjectProperty()
    first_step_min_input: ObjectProperty()
    first_step_max_input: ObjectProperty()
    first_step_attempts_input: ObjectProperty()
    second_step_min_input: ObjectProperty()
    second_step_max_input: ObjectProperty()
    second_step_attempts_input: ObjectProperty()
    random_smoothing_input: ObjectProperty()
    cave_system: CaveGenerator

    def update_settings(self):
        print(f"update settings {self}")

    def create_new_map(self):
        self.initialize_map()

        for _ in range(int(self.first_step_attempts)):
            self.cave_system.smooth_step(
                min_count=int(self.first_step_min), max_count=self.first_step_max
            )

        for _ in range(int(self.second_step_attempts)):
            self.cave_system.smooth_step(
                min_count=self.second_step_min, max_count=self.second_step_max
            )

        self.map_to_image()

    def initialize_map(self):
        new_cave = CaveGenerator()
        new_cave.height = self.map_height
        new_cave.width = self.map_width

        new_cave.initialize_map()
        self.cave_system = new_cave

    def first_smooth_step(self):
        self.cave_system.smooth_step(
            min_count=self.first_step_min, max_count=self.first_step_max
        )
        self.map_to_image()

    def second_smooth_step(self):
        self.cave_system.smooth_step(
            min_count=self.second_step_min, max_count=self.second_step_max
        )
        self.map_to_image()

    def random_smoothing(self):
        self.initialize_map()
        self.cave_system.random_smoothing(attempts=self.random_smoothing_attempts)
        self.map_to_image()

    def map_to_image(self):
        self.cave_system.map_to_image()
        self.map_image.reload()

    @property
    def random_smoothing_attempts(self) -> int:
        return int(self.random_smoothing_input.text)

    @property
    def map_height(self) -> int:
        return int(self.map_height_input.text)

    @property
    def map_width(self) -> int:
        return int(self.map_width_input.text)

    @property
    def first_step_attempts(self) -> int:
        return int(self.first_step_attempts_input.text)

    @property
    def first_step_min(self) -> int:
        return int(self.first_step_min_input.text)

    @property
    def first_step_max(self) -> int:
        return int(self.first_step_max_input.text)

    @property
    def second_step_attempts(self) -> int:
        return int(self.second_step_attempts_input.text)

    @property
    def second_step_min(self) -> int:
        return int(self.second_step_min_input.text)

    @property
    def second_step_max(self) -> int:
        return int(self.second_step_max_input.text)


class MapGeneratorApp(kv_app.App):
    def build(self):
        return MapGenerator()


if __name__ == "__main__":
    MapGeneratorApp().run()
