import pygame
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SNAKE_SIZE = 20
FPS = 10

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Snake:
    def __init__(self):
        self.size = SNAKE_SIZE
        self.body = [(100, 100)]
        self.direction = (1, 0)

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0] * SNAKE_SIZE,
                    head_y + self.direction[1] * SNAKE_SIZE)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True
        if (head_x, head_y) in self.body[1:]:
            return True
        return False

    def set_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

class Food:
    def __init__(self):
        self.position = self._random_position()

    def _random_position(self):
        return (random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE,
                random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)

    def spawn(self):
        self.position = self._random_position()

def play_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((1, 0))

        snake.move()

        if snake.body[0] == food.position:
            snake.grow()
            food.spawn()

        if snake.check_collision():
            running = False

        screen.fill(BLACK)
        for block in snake.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food.position[0], food.position[1], SNAKE_SIZE, SNAKE_SIZE))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    play_game()
