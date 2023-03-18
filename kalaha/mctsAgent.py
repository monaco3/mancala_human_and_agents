import random
from kalaha.agent import Agent
from kalaha.player import Player

class MCTSAgent(Agent):
    def __init__(self, num_simulations=1000):
        self.num_simulations = num_simulations

    def choose(self, input_game) -> int:
        best_move = -1
        best_score = -1

        for move in input_game.get_possible_moves():
            total_score = 0
            game_copy = copy.deepcopy(input_game)
            game_copy.move_marbles(move)

            for _ in range(self.num_simulations):
                sim_game = copy.deepcopy(game_copy)
                while sim_game.winner == Player.BLANK:
                    sim_game.move_marbles(random.choice(sim_game.get_possible_moves()))
                if sim_game.winner == input_game.current_player:
                    total_score += 1

            avg_score = total_score / self.num_simulations
            if avg_score > best_score:
                best_score = avg_score
                best_move = move

        return best_move

    def __str__(self):
        return "MCTS Agent"
