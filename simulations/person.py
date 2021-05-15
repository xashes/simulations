#!/usr/bin/env python3

import arcade as ac


class PersonSprite(ac.Sprite):
    def __init__(self):
        super().__init__()

        self.dead_zone = 0.1

        # constants used to track if the player if facing left or right
        self.right_facing = 0
        self.left_facing = 1

        self.distance_to_change_texture = 20

        self.scale = 0.5

        # Images from Kenney.nl's Character pack
        # main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = ac.load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = ac.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = ac.load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = ac.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        self.character_face_direction = self.right_facing

        self.cur_texture = 0

        # how far have we traveled horizontally since changing the texture
        self.x_odometer = 0

    def pymunk_moved(self, physics_engine: ac.PymunkPhysicsEngine, dx, dy, d_angle):
        if dx < -self.dead_zone and self.character_face_direction == self.right_facing:
            self.character_face_direction = self.left_facing
        elif dx > self.dead_zone and self.character_face_direction == self.left_facing:
            self.character_face_direction = self.right_facing

        is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometer += dx

        # Jumping animation
        if not is_on_ground:
            if dy > self.dead_zone:
                self.texture = self.jump_texture_pair[self.character_face_direction]
            elif dy < -self.dead_zone:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return

        if abs(dx) <= self.dead_zone:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        if abs(self.x_odometer) > self.distance_to_change_texture:

            self.x_odometer = 0

            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][
                self.character_face_direction
            ]
