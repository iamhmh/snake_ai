import pygame
import neat
import os
import random

# Paramètres de l'écran et du jeu
SCREEN_WIDTH = 1200  # Augmenté pour tenir plusieurs jeux
SCREEN_HEIGHT = 800
SNAKE_SIZE = 20
FPS = 10
NUM_GAMES = 4  # Nombre de jeux simultanés (divisé sur la fenêtre)

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class SnakeGameAI:
    def __init__(self, offset_x=0, offset_y=0):
        self.snake = [(100, 100)]
        self.direction = (1, 0)
        self.food = self._random_food_position()
        self.frame_iteration = 0
        self.score = 0
        self.offset_x = offset_x  # Décalage pour gérer les multiples jeux
        self.offset_y = offset_y


    def _random_food_position(self):
        return (random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE,
                random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)

    def move(self, action):
        clockwise_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        current_idx = clockwise_directions.index(self.direction)

        if action == 0:  # tourner à gauche
            new_idx = (current_idx - 1) % 4
        elif action == 1:  # aller tout droit
            new_idx = current_idx
        else:  # tourner à droite
            new_idx = (current_idx + 1) % 4

        self.direction = clockwise_directions[new_idx]

        # Mouvements du serpent
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0] * SNAKE_SIZE,
                    head_y + self.direction[1] * SNAKE_SIZE)
        self.snake = [new_head] + self.snake[:-1]

    def is_collision(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True
        if (head_x, head_y) in self.snake[1:]:
            return True
        return False

    def play_step(self, action):
        self.frame_iteration += 1
        self.move(action)

        # Calcul de la distance avant et après le mouvement par rapport à la nourriture
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        distance_before = abs(head_x - food_x) + abs(head_y - food_y)

        # Vérifier si le serpent a mangé la nourriture
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])  # Agrandir le serpent
            self.food = self._random_food_position()
            self.score += 10  # Récompense significative pour avoir mangé une pomme
            return False, self.score + 500  # Récompense encore plus importante pour encourager ce comportement

        # Vérifier si le serpent entre en collision avec un mur ou son corps
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            return True, self.score  # Pénalité en cas de collision ou trop d'itérations sans progrès

        # Ajout d'une pénalité si le serpent tourne en rond ou ne progresse pas
        if self.frame_iteration > 200 and distance_after >= distance_before:
            return True, -100  # Pénalité pour comportement inefficace ou répétitif

        # Calcul de la distance après le mouvement
        distance_after = abs(self.snake[0][0] - food_x) + abs(self.snake[0][1] - food_y)

        # Récompense ou pénalité en fonction du rapprochement ou éloignement de la nourriture
        if distance_after < distance_before:
            reward = 5  # Augmenter la récompense pour se rapprocher de la nourriture
        else:
            reward = -5  # Pénalité plus sévère pour s'en éloigner

        return False, reward

    def get_state(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        direction_x, direction_y = self.direction

        # Distances relatives à la nourriture
        food_distance_x = abs(food_x - head_x) / SCREEN_WIDTH  # Distance normalisée entre 0 et 1
        food_distance_y = abs(food_y - head_y) / SCREEN_HEIGHT

        # Indiquer si la nourriture est dans une direction spécifique
        food_right = food_x > head_x
        food_left = food_x < head_x
        food_up = food_y < head_y
        food_down = food_y > head_y

        # Dangers imminents (mur ou corps du serpent)
        danger_straight = self._is_danger_straight()
        danger_left = self._is_danger_left()
        danger_right = self._is_danger_right()

        # Distances aux murs (en cellules)
        distance_up = head_y // SNAKE_SIZE
        distance_down = (SCREEN_HEIGHT - head_y) // SNAKE_SIZE
        distance_left = head_x // SNAKE_SIZE
        distance_right = (SCREEN_WIDTH - head_x) // SNAKE_SIZE

        # Créer un état complet
        state = [
            danger_straight, danger_left, danger_right,
            food_left, food_right, food_up, food_down,
            food_distance_x, food_distance_y,  # Ajout des distances relatives normalisées
            distance_up, distance_down, distance_left, distance_right,
            direction_x, direction_y
        ]

        return state


    def _is_danger_straight(self):
        head_x, head_y = self.snake[0]
        next_pos = (head_x + self.direction[0] * SNAKE_SIZE, head_y + self.direction[1] * SNAKE_SIZE)
        return self.is_collision_position(next_pos)

    def _is_danger_left(self):
        left_direction = (-self.direction[1], self.direction[0])  # Tourner à gauche
        head_x, head_y = self.snake[0]
        next_pos = (head_x + left_direction[0] * SNAKE_SIZE, head_y + left_direction[1] * SNAKE_SIZE)
        return self.is_collision_position(next_pos)

    def _is_danger_right(self):
        right_direction = (self.direction[1], -self.direction[0])
        head_x, head_y = self.snake[0]
        next_pos = (head_x + right_direction[0] * SNAKE_SIZE, head_y + right_direction[1] * SNAKE_SIZE)
        return self.is_collision_position(next_pos)

    def is_collision_position(self, pos):
        x, y = pos
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return True
        if pos in self.snake[1:]:
            return True
        return False


def eval_genomes(genomes, config):
    best_genome = None
    best_fitness = -1
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Définir les positions de chaque jeu sur l'écran
    game_positions = [(0, 0), (SCREEN_WIDTH // 2, 0), (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

    for idx, (genome_id, genome) in enumerate(genomes):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = SnakeGameAI(offset_x=game_positions[idx % 4][0], offset_y=game_positions[idx % 4][1])  # Assigner une position
        fitness = 0

        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            state = game.get_state()
            action = net.activate(state)
            action_idx = action.index(max(action))
            done, score = game.play_step(action_idx)

            fitness += score
            if done:
                break

        genome.fitness = fitness

        if fitness > best_fitness:
            best_fitness = fitness
            best_genome = genome

    if best_genome is not None:
        net = neat.nn.FeedForwardNetwork.create(best_genome, config)
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            for idx in range(NUM_GAMES):
                game = SnakeGameAI(offset_x=game_positions[idx][0], offset_y=game_positions[idx][1])
                state = game.get_state()
                action = net.activate(state)
                action_idx = action.index(max(action))
                done, score = game.play_step(action_idx)

                # Afficher chaque jeu dans sa position respective
                screen.fill(BLACK)
                for block in game.snake:
                    pygame.draw.rect(screen, GREEN, pygame.Rect(block[0] + game.offset_x, block[1] + game.offset_y, SNAKE_SIZE, SNAKE_SIZE))
                pygame.draw.rect(screen, RED, pygame.Rect(game.food[0] + game.offset_x, game.food[1] + game.offset_y, SNAKE_SIZE, SNAKE_SIZE))

            pygame.display.flip()
            clock.tick(FPS)

            if done:
                running = False

def run_neat(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(eval_genomes, 1000)

if __name__ == "__main__":
    pygame.init()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run_neat(config_path)
    pygame.quit()
