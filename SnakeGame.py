import pygame
import Constants
from Elements import *

# 游戏常量
SCREEN_WIDTH = Constants.SCREEN_WIDTH
SCREEN_HEIGHT = Constants.SCREEN_HEIGHT
PANEL_HEIGHT = Constants.PANEL_HEIGHT
BLOCK_SIZE = Constants.BLOCK_SIZE

# 颜色常量
BLACK = Constants.BLACK
GRAY = Constants.GRAY
WHITE = Constants.WHITE
RED = Constants.RED
GREEN = Constants.GREEN
BLUE = Constants.BLUE

# 其他常量
FRAME = 1000 // Constants.SPEED
GAME_WIDTH = SCREEN_WIDTH
GAME_HEIGHT = SCREEN_HEIGHT - PANEL_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake)
        self.score = 0
        self.try_count = 1
        self.font = pygame.font.SysFont('Minecraft Regular', 20)
        self.menu = Menu(self.screen)
        self.settings = Settings(self.screen)
        self.state = 'startmenu'

    def update(self, direction):
        self.snake.direction = direction
        self.snake.move(self.food)
        if self.snake.check_game_over():
            self.try_count += 1
            self.state = 'gameover'
        self.score = self.snake.length - 1

    def draw(self):
        self.screen.fill(BLACK)
        for block in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, RED, (self.food.position[0], self.food.position[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.line(self.screen, WHITE, (0, GAME_HEIGHT), (GAME_WIDTH, GAME_HEIGHT), 2)
        # 创建一个文本Surface对象
        score_surface = self.font.render('Score: {}'.format(self.score), True, WHITE)
        # 获取文本Surface对象的矩形区域
        score_rect = score_surface.get_rect()
        # 将文本Surface对象居中放置在屏幕底部
        score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - PANEL_HEIGHT // 2)
        # 将文本Surface对象绘制到屏幕上
        self.screen.blit(score_surface, score_rect)
        pygame.display.update()

    def run(self):
        tick = FRAME
        direction = self.snake.direction
        while True:
            if self.state == 'playing':
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
            elif self.state == 'startmenu':
                self.menu.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    action = self.menu.handle_event(event)
                    if action == 'start':
                        self.state = 'playing'
                    elif action == 'settings':
                        self.state = 'settings'
                    elif action == 'quit':
                        pygame.quit()
                        quit()
            elif self.state == 'settings':
                self.settings.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    action = self.settings.handle_event(event)
                    if action == 'back':
                        if self.try_count == 1:
                            self.state = 'startmenu'
                        else:
                            self.state = 'gameover'
            elif self.state == 'gameover':
                self.menu.selected_button = 0
                while self.state == 'gameover':
                    self.menu.buttons[0]['text'] = 'Restart Game'
                    self.menu.draw()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        action = self.menu.handle_event(event)
                        if action == 'start':
                            self.snake = Snake()
                            self.food = Food()
                            self.food.spawn(self.snake)
                            self.score = 0
                            self.state = 'playing'
                        elif action == 'settings':
                            self.state = 'settings'
                        elif action == 'quit':
                            pygame.quit()
                            quit()
            else:
                pygame.quit()
                quit()
            # tick -= self.clock.tick(60)
