import random
import Constants

# 游戏常量
BLOCK_SIZE = Constants.BLOCK_SIZE

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
