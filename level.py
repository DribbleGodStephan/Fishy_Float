import pygame
from settings import *
from tile import Tile
from player import Player

# creates level class
class Level:

    def __init__(self, level_data, surface):

        #setting Level variables
        #play music
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.setup_level(level_data)
        self.score = 0
        pygame.mixer.music.load("music/funky_underwater.mp3")
        pygame.mixer.music.play(-1)

        self.world_shift = 0
        self.screen_status = "still"

    # function that reads the contents of the level
    def setup_level(self, layout):

        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                x = cell_index * tile_size
                y = row_index * tile_size - 200
                if cell == "x":
                    tile_sprite = Tile((x,y), tile_size)
                    self.tiles.add(tile_sprite)
                elif cell == "p":
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

    # function that scrolls the screen vertically
    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        jump_speed = player.jump_speed


        if self.screen_status != "scroll_down" and (player.status == "jump" or player.status == "swim"):
            self.world_shift = 4
            self.screen_status = "scroll_up"

        elif self.screen_status != "scroll_up":
            if player_y > screen_height:
                self.world_shift = -30
                self.screen_status = "scroll_down"

            elif player_y < screen_height - (player.image.get_height() * 1.5):
                self.world_shift = 0
                self.screen_status = "still"

    # function that calculates and displays the score based on the player's vertical movement
    def calculate_score(self,screen):

        player = self.player.sprite
        player_y = player.rect.centery
        if player.direction.y < 0:
            self.score -= round(player.direction.y)
        if player_y < screen_height:
            self.draw_text("Score: " + str(self.score),pygame.font.Font("/Users/stephantinel/PycharmProjects/ScubaFloat/font/Baloo_2/Baloo2-VariableFont_wght.ttf", 40), (255, 255, 255), screen_width-230, screen_height-720,screen)


    # function that chnages the screen black and displayy the score when the player has lost
    def lose(self,screen):

        player = self.player.sprite
        player_y = player.rect.centery
        if self.screen_status == "scroll_up" and player_y > screen_height:
            screen.fill("black")
            self.draw_text("Score: " + str(self.score),pygame.font.Font("/Users/stephantinel/PycharmProjects/ScubaFloat/font/Baloo_2/Baloo2-VariableFont_wght.ttf", 100), (255, 255, 255), screen_width/2-200, screen_height/2-100,screen)

    # function that displays draws all text
    def draw_text(self,text, font, text_col, x, y,screen):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    # function that repeatedly updates functions
    def run(self,screen):

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_y()
        self.player.update(self.tiles,screen)
        self.scroll_y()
        self.player.draw(self.display_surface)
        self.lose(screen)
        self.calculate_score(screen)
