import pygame
import random
import Constants

# 游戏常量
BLOCK_SIZE = Constants.BLOCK_SIZE
SCREEN_WIDTH = Constants.SCREEN_WIDTH
SCREEN_HEIGHT = Constants.SCREEN_HEIGHT
DIFFICULTY = Constants.DIFFICULTY
SNAKE_DISPLAY = Constants.SNAKE_DISPLAY
SPEED = Constants.SPEED

# 颜色常量
BLACK = Constants.BLACK
GRAY = Constants.GRAY
WHITE = Constants.WHITE
RED = Constants.RED
GREEN = Constants.GREEN
BLUE = Constants.BLUE
YELLOW = Constants.YELLOW

# 其他常量
GAME_WIDTH = Constants.SCREEN_WIDTH
GAME_HEIGHT = Constants.SCREEN_HEIGHT - Constants.PANEL_HEIGHT


class Snake:
    def __init__(self):
        self.body = [((GAME_WIDTH // 2 // BLOCK_SIZE) * BLOCK_SIZE, (GAME_HEIGHT // 2 // BLOCK_SIZE) * BLOCK_SIZE)]
        self.direction = 'right'
        self.length = 1

    def move(self, food):
        x, y = self.body[0]
        if self.direction == 'up':
            y -= BLOCK_SIZE
        elif self.direction == 'down':
            y += BLOCK_SIZE
        elif self.direction == 'left':
            x -= BLOCK_SIZE
        elif self.direction == 'right':
            x += BLOCK_SIZE
        self.body.insert(0, (x, y))
        if (x, y) == food.position:
            self.length += 1
            food.spawn(self)
        else:
            self.body.pop()

    def check_game_over(self):
        x, y = self.body[0]
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        for block in self.body[1:]:
            if block == self.body[0]:
                return True
        return False


class Food:
    def __init__(self):
        self.position = (0, 0)

    def spawn(self, snake):
        x = random.randint(0, GAME_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
        y = random.randint(0, GAME_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
        while not self.check_position(x, y, snake):
            x = random.randint(0, GAME_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
            y = random.randint(0, GAME_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.position = (x, y)

    def check_position(self, x, y, snake):
        for body_block in snake.body[:]:
            if body_block == (x, y):
                return False
        return True


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont('Minecraft Regular', 48)
        self.score_font = pygame.font.SysFont('Minecraft Regular', 16, italic=True)
        self.font = pygame.font.SysFont('Minecraft Regular', 24)
        self.buttons = [
            {'text': 'Start Game', 'action': 'start'},
            {'text': 'Settings', 'action': 'settings'},
            {'text': 'Quit Game', 'action': 'quit'}
        ]
        self.title = 'Snake'
        self.your_score = 'by Imiloin'
        self.selected_button = 0

    def draw(self):
        self.screen.fill(BLACK)
        # 绘制标题
        title_surface = self.title_font.render(self.title, True, BLUE)
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.screen.blit(title_surface, title_rect)
        # 绘制分数
        score_surface = self.score_font.render(self.your_score, True, GRAY)
        score_rect = score_surface.get_rect()
        score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.screen.blit(score_surface, score_rect)
        for i, button in enumerate(self.buttons):
            text_surface = self.font.render(button['text'], True, WHITE if i == self.selected_button else GRAY)
            text_rect = text_surface.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 * 2 + i * 48)
            self.screen.blit(text_surface, text_rect)
        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.buttons[self.selected_button]['action']
        return None


class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Minecraft Regular', 24)
        # 读取配置文件
        with open('config.ini', 'r') as f:
            lines = f.readlines()
        saved_settings = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=')
                saved_settings[key.strip()] = value.strip()
        Difficulty = int(saved_settings.get('Difficulty', '0'))
        Snake_Display = int(saved_settings.get('Snake_Display', '0'))
        self.options = [
            {'text': 'Difficulty', 'current_level': DIFFICULTY[Difficulty], 'current_index': Difficulty, 'min': 0,
             'max': len(DIFFICULTY) - 1, 'option_type': DIFFICULTY},
            {'text': 'Snake Display', 'current_level': SNAKE_DISPLAY[Snake_Display], 'current_index': Snake_Display,
             'min': 0, 'max': len(SNAKE_DISPLAY) - 1, 'option_type': SNAKE_DISPLAY}
        ]
        self.speed = SPEED[Difficulty]
        self.selected_option = 0

    def draw(self):
        self.screen.fill(BLACK)
        for i, option in enumerate(self.options):
            text_surface = self.font.render('{}: {}'.format(option['text'], option['current_level']), True,
                                            WHITE if i == self.selected_option else GRAY)
            text_rect = text_surface.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 48)
            self.screen.blit(text_surface, text_rect)
        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                option = self.options[self.selected_option]
                option['current_index'] = max(option['min'], option['current_index'] - 1)
                option['current_level'] = option['option_type'][option['current_index']]
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                option = self.options[self.selected_option]
                option['current_index'] = min(option['max'], option['current_index'] + 1)
                option['current_level'] = option['option_type'][option['current_index']]
            elif event.key == pygame.K_ESCAPE:
                return 'back'
        return None

    def save_settings(self):
        self.speed = SPEED[self.options[0]['current_index']]
        with open('config.ini', 'w') as f:
            for option in self.options:
                f.write('{} = {}\n'.format(option['text'].replace(' ', '_'), option['current_index']))
