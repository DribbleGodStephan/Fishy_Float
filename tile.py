import pygame
import random
from support import import_folder

# creation of tile class
class Tile(pygame.sprite.Sprite):

    # randomize fish
    def __init__(self, pos, size):
        super().__init__()
        fish_n = random.randint(1,30)
        if fish_n <= 24:
            self.fish = "fish_1"
        elif fish_n <= 29:
            self.fish = "fish_2"
        else:
            self.fish = "fish_3"

    # setting Tile variables
        self.animations = {}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = random.randint(1,5) / 10

        self.image = self.animations[self.fish][self.frame_index]
        self.image = pygame.transform.scale(self.image, (160,80))
        self.rect = self.image.get_rect(topleft=pos)
        self.flip = random.randint(1,2)

    # function that updates position and animation of fish
    def update(self, y_shift):
        self.rect.y += y_shift
        self.animate()

    # function that animates the fish
    def animate(self):
        animation = self.animations[self.fish]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

        if self.flip == 2:
            # Flip image
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)

        self.image = pygame.transform.scale(self.image, (200, 100))

    # function that imports fish animations
    def import_character_assets(self):
        character_path = "graphics/fish/"

        self.animations = {"fish_1":[], "fish_2":[], "fish_3": []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

