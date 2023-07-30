import pygame
from Elements import Snake, Food

# 游戏常量
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 10
SPEED = 5
FRAME = 1000 // SPEED

# 颜色常量
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake)

    def update(self, direction):
        self.snake.direction = direction
        self.snake.move(self.food)
        if self.snake.check_game_over():
            pygame.quit()
            quit()

    def draw(self):
        self.screen.fill(BLACK)
        for block in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, RED, (self.food.position[0], self.food.position[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()

    def run(self):
        tick = FRAME
        direction = self.snake.direction
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.snake.direction != 'down':
                        direction = 'up'
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.snake.direction != 'up':
                        direction = 'down'
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.snake.direction != 'right':
                        direction = 'left'
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.snake.direction != 'left':
                        direction = 'right'
                    if tick < FRAME / 2:
                        tick = FRAME
                        self.update(direction)
                        self.draw()
                    pygame.time.delay(10)
            if tick <= 0:
                tick = FRAME
                self.update(direction)
                self.draw()
            else:
                pygame.time.delay(10)
                tick -= 10
