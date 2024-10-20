# Snake AI with NEAT and Pygame

This project demonstrates the use of NEAT (NeuroEvolution of Augmenting Topologies) and Pygame to create an AI that plays the classic Snake game. The AI is developed in Python and uses the NEAT algorithm to evolve neural networks over generations.

## Project Overview

- **Language**: Python
- **Libraries**: NEAT, Pygame

## How It Works

1. **NEAT Algorithm**: NEAT is used to evolve neural networks. It starts with a population of simple networks and evolves them over generations to improve their performance.
2. **Pygame**: Pygame is used to create the Snake game environment where the AI plays.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/iamhmh/snake_ai.git
    ```
2. Install the required libraries:
    ```sh
    pip install neat-python pygame
    ```

## Running the Project

To run the project, execute the following command in the `env` folder:
```sh
python ai_snake.py
```

## Project Structure

- `ai_snake.py`: The main script to run the AI.
- `config-feedforward.txt`: Configuration file for the NEAT algorithm.
- `snake.py`: Contains the logic for the Snake game (starting point for building the game).

## Acknowledgements

- [NEAT-Python](https://neat-python.readthedocs.io/en/latest/)
- [Pygame](https://www.pygame.org/)

## License

This project is licensed under the MIT License.

## Author

- **HICHEM GOUIA** - (https://github.com/iamhmh)