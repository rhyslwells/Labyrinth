# renderer.py
import pygame
from PIL import Image
import numpy as np

WIDTH, HEIGHT = 800, 800
FPS = 60

class Renderer:
    def __init__(self, grid, actor, delay=0):
        self.grid = grid
        self.actor = actor
        self.delay = delay
        self._init_rendering()

    def _init_rendering(self):
        sprite_dims_x = WIDTH // self.grid.shape[0]
        sprite_dims_y = HEIGHT // self.grid.shape[1]

        self.GROUND_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.GROUND_SPRITE.fill((255, 255, 255))  # White

        self.WALL_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.WALL_SPRITE.fill((0, 0, 0))  # Black

        self.START_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.START_SPRITE.fill((0, 255, 0))  # Green

        self.GOAL_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.GOAL_SPRITE.fill((255, 0, 0))  # Red

        self.Actor_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.Actor_SPRITE.fill((0, 0, 255))  # Blue

        self.render_mode = False
        self.window = None
        self.clock = None

    def render(self):
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()

        self.window.fill((0, 0, 0))
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                sprite_to_draw = self.GROUND_SPRITE
                if col == 'w':
                    sprite_to_draw = self.WALL_SPRITE
                elif col == 's':
                    sprite_to_draw = self.START_SPRITE
                elif col == 't':
                    sprite_to_draw = self.GOAL_SPRITE
                self.window.blit(sprite_to_draw, (x * (WIDTH // self.grid.shape[0]), y * (HEIGHT // self.grid.shape[1])))

        self.window.blit(self.Actor_SPRITE, (self.actor.position[0] * (WIDTH // self.grid.shape[0]), self.actor.position[1] * (HEIGHT // self.grid.shape[1])))
        self.clock.tick(FPS)
        pygame.display.flip()

    def save_grid_to_image(self, filename: str):
        color_map = {
            'w': (0, 0, 0),   # Black for walls
            '.': (255, 255, 255),  # White for empty spaces
            's': (0, 255, 0),  # Green for start
            't': (255, 0, 0),  # Red for goal
            'A': (0, 0, 255)   # Blue for actor
        }
        cell_size = 20
        image_data = np.zeros((self.grid.shape[1] * cell_size, self.grid.shape[0] * cell_size, 3), dtype=np.uint8)
        
        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                color = color_map.get(self.grid[y, x], (255, 255, 255))
                image_data[y * cell_size:(y + 1) * cell_size, x * cell_size:(x + 1) * cell_size] = color
        
        img = Image.fromarray(image_data)
        img.save(filename)
