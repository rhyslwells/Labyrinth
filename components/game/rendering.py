import pygame

class GameWindow:
    def __init__(self, game, width=800, height=800, fps=60):
        self.game = game
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.width = width
        self.height = height

    def render(self):
        self.window.fill((0, 0, 0))  # Fill the background with black
        sprite_dims_x = self.width // self.game.env.shape[0]
        sprite_dims_y = self.height // self.game.env.shape[1]
        
        for x, row in enumerate(self.game.env):
            for y, col in enumerate(row):
                if col == 'w':
                    pygame.draw.rect(self.window, (0, 0, 0), (x * sprite_dims_x, y * sprite_dims_y, sprite_dims_x, sprite_dims_y))  # Draw walls in black
                elif col == 's':
                    pygame.draw.rect(self.window, (0, 255, 0), (x * sprite_dims_x, y * sprite_dims_y, sprite_dims_x, sprite_dims_y))  # Draw start in green
                elif col == 't':
                    pygame.draw.rect(self.window, (255, 0, 0), (x * sprite_dims_x, y * sprite_dims_y, sprite_dims_x, sprite_dims_y))  # Draw goal in red
                else:
                    pygame.draw.rect(self.window, (255, 255, 255), (x * sprite_dims_x, y * sprite_dims_y, sprite_dims_x, sprite_dims_y))  # Draw empty spaces in white
        
        actor_pos = self.game.current_pos
        pygame.draw.rect(self.window, (0, 0, 255), (actor_pos[0] * sprite_dims_x, actor_pos[1] * sprite_dims_y, sprite_dims_x, sprite_dims_y))  # Draw actor in blue
        
        pygame.display.flip()
        self.clock.tick(self.fps)
