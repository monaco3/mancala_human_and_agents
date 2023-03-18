import random
from kalaha.agent import Agent

class RandomAgent(Agent):
    def choose(self, input_game) -> int:
        return random.choice(input_game.get_possible_moves())

    def __str__(self):
        return "Random Agent"
