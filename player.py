import pygame
from settings import *
from support import import_folder

# creation of player class
class Player(pygame.sprite.Sprite):

    def __init__ (self,pos):
        super().__init__()

        # setting player variables
        self.animations = {}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.05

        self.image = self.animations["idle"][self.frame_index]
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 15
        self.jump_speed = -35
        self.gravity = 3

        self.status = "idle"

    # function that runs the correct player animations
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        if self.direction.x < 0:
            # Flip image
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)
        if self.direction.y < 0:
            self.image = pygame.transform.rotozoom(animation[int(self.frame_index)],90,1)
        else:
            self.image = animation[int(self.frame_index)]

        self.image = pygame.transform.scale(self.image, (100, 100))

    # function that imports player animations
    def import_character_assets(self):
        character_path = "graphics/player/"

        self.animations = {"idle":[], "swim":[], "jump": []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # function that allows the player to move based on the keys pressed
    def get_input(self,screen):
        keys = pygame.key.get_pressed()

        if self.rect.y < screen_height:

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1

            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE] and self.direction.y == 0:
                self.jump()

    # function that gets the player's current movement status
    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        else:
            if self.direction.x == 0:
                self.status = "idle"
            else:
                self.status = "swim"

    # function that allows the user to jump
    def jump(self):
        if self.status != "jump":

            self.direction.y = self.jump_speed

    # function that the user to move horizontally with the correct speed
    def horizontal_movement(self):
        self.rect.x += self.direction.x * self.speed

    # function that allows for tile collision vertically
    def vertical_movement_collisions(self, tiles):
        self.apply_gravity()

        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.direction.y = 0
                    self.effect_on_player(tile.fish)

    # function that applies the effects of different fish on the player
    def effect_on_player(self,fish):

        if fish == "fish_1":
            self.gravity = 3
            self.animation_speed = 0.05
            self.speed = 15
        elif fish == "fish_2":
            self.gravity = 2.25
            self.animation_speed = 0.0375
        elif fish == "fish_3":
            self.speed = 30

    # function that applies gravity
    def apply_gravity(self):

        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # function that repeatedly updates other player functions
    def update(self, tiles,screen):
        self.get_input(screen)
        self.horizontal_movement()
        self.vertical_movement_collisions(tiles)
        self.get_status()
        self.animate()

