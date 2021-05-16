#!/usr/bin/env python3

import arcade as ac
from typing import Optional
from simulations.person import PersonSprite

title = "道德"

sprite_image_size = 128

sprite_scaling_player = 0.5
sprite_scaling_tiles = 0.5

sprite_size = int(sprite_image_size * sprite_scaling_player)

# Size of grid to show on screen, in number of tiles
screen_grid_width = 25
screen_grid_height = 15

width = sprite_size * screen_grid_width
height = sprite_size * screen_grid_height

default_gravity = 1500

# Gamping - amount of speed lost per second
default_damping = 1
player_damping = 0.4

player_friction = 1.0
wall_friction = 0.7
dynamic_item_friction = 0.6

player_mass = 2

player_max_horizontal_speed = 450
player_max_vertical_speed = 1600

player_move_force_on_ground = 8000
player_move_force_in_air = 900
player_jump_impulse = 1800


class GameWindow(ac.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.player_sprite: Optional[ac.Sprite] = None

        # Sprite Lists
        self.player_list: Optional[PersonSprite] = None
        self.wall_list: Optional[ac.SpriteList] = None
        self.bullet_list: Optional[ac.SpriteList] = None
        self.item_list: Optional[ac.SpriteList] = None

        # Track the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False

        ac.set_background_color(ac.color.AMAZON)

    def setup(self):
        self.player_list = ac.SpriteList()
        self.bullet_list = ac.SpriteList()

        map_name = "./resources/map.tmx"
        my_map = ac.tilemap.read_tmx(map_name)

        self.wall_list = ac.tilemap.process_layer(
            my_map, "Platforms", sprite_scaling_tiles
        )
        self.item_list = ac.tilemap.process_layer(
            my_map, "Dynamic Items", sprite_scaling_tiles
        )

        self.player_sprite = PersonSprite()
        # set player location
        grid_x = 1
        grid_y = 1
        self.player_sprite.center_x = sprite_size * grid_x + sprite_size / 2
        self.player_sprite.center_y = sprite_size * grid_y + sprite_size / 2

        self.player_list.append(self.player_sprite)

        # Engine setup
        damping = default_damping

        gravity = (0, -default_gravity)

        self.physics_engine = ac.PymunkPhysicsEngine(damping=damping, gravity=gravity)

        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=player_friction,
            mass=player_mass,
            moment=ac.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            max_horizontal_velocity=player_max_horizontal_speed,
            max_vertical_velocity=player_max_vertical_speed,
        )

        self.physics_engine.add_sprite_list(
            self.wall_list,
            friction=wall_friction,
            collision_type="wall",
            body_type=ac.PymunkPhysicsEngine.STATIC,
        )

        self.physics_engine.add_sprite_list(
            self.item_list, friction=dynamic_item_friction, collision_type="item"
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == ac.key.LEFT:
            self.left_pressed = True
        elif symbol == ac.key.RIGHT:
            self.right_pressed = True
        elif symbol == ac.key.UP:
            if self.physics_engine.is_on_ground(self.player_sprite):
                impulse = (0, player_jump_impulse)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == ac.key.LEFT:
            self.left_pressed = False
        elif symbol == ac.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time: float):
        """ Movement and game logic """
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        if self.left_pressed and not self.right_pressed:
            if is_on_ground:
                force = (-player_move_force_on_ground, 0)
            else:
                force = (-player_move_force_in_air, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            if is_on_ground:
                force = (player_move_force_on_ground, 0)
            else:
                force = (player_move_force_in_air, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            self.physics_engine.set_friction(self.player_sprite, 1)

        self.physics_engine.step()

    def on_draw(self):
        ac.start_render()

        self.wall_list.draw()
        self.bullet_list.draw()
        self.item_list.draw()
        self.player_list.draw()


def main():
    window = GameWindow(width, height, title)
    window.setup()
    ac.run()


if __name__ == "__main__":
    main()
