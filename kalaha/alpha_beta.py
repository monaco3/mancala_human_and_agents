import copy

from kalaha.agent import Agent
from kalaha.player import Player

class AlphaBetaMinimaxAgent(Agent):
    def __init__(self):
        self.max_depth = None

    def choose(self, input_game) -> int:
        alpha = -float('inf')
        beta = float('inf')
        minimax = self.alphabeta(input_game, 0, alpha, beta)
        print(self.__str__(), "player chooses:", minimax)
        return minimax

    def alphabeta(self, input_game, depth: int, alpha: float, beta: float) -> int:
        best_move = -1
        game = copy.deepcopy(input_game)

        if game.current_player == Player.TOP:
            maximum_score = -48
            for i in game.get_possible_moves():
                game_copy = copy.deepcopy(game)
                game_copy.move_marbles(i)
                score = self.min_value(game_copy, depth + 1, alpha, beta)
                if score > maximum_score:
                    maximum_score = score
                    best_move = i
                alpha = max(alpha, maximum_score)
                if beta <= alpha:
                    break

        elif game.current_player == Player.BOTTOM:
            minimum_score = 48
            for i in game.get_possible_moves():
                game_copy = copy.deepcopy(game)
                game_copy.move_marbles(i)
                score = self.max_value(game_copy, depth + 1, alpha, beta)
                if score < minimum_score:
                    minimum_score = score
                    best_move = i
                beta = min(beta, minimum_score)
                if beta <= alpha:
                    break

        return best_move

    def max_value(self, input_game, depth: int, alpha: float, beta: float) -> int:
        if input_game.winner != Player.BLANK:
            return input_game.get_score()
        if depth == self.max_depth:
            return input_game.get_score()

        maximum_score = -48
        game = copy.deepcopy(input_game)
        for i in game.get_possible_moves():
            game_copy = copy.deepcopy(game)
            game_copy.move_marbles(i)
            if game.current_player == Player.TOP:
                score = self.min_value(game_copy, depth + 1, alpha, beta)
            else:
                score = self.max_value(game_copy, depth + 1, alpha, beta)
            maximum_score = max(maximum_score, score)
            alpha = max(alpha, maximum_score)
            if beta <= alpha:
                break
        return maximum_score

    def min_value(self, input_game, depth: int, alpha: float, beta: float) -> int:
        if input_game.winner != Player.BLANK:
            return input_game.get_score()
        if depth == self.max_depth:
            return input_game.get_score()

        minimum_score = 48
        game = copy.deepcopy(input_game)
        for i in game.get_possible_moves():
            game_copy = copy.deepcopy(game)
            game_copy.move_marbles(i)
            if game.current_player == Player.TOP:
                score = self.min_value(game_copy, depth + 1, alpha, beta)
            else:
                score = self.max_value(game_copy, depth + 1, alpha, beta)
            minimum_score = min(minimum_score, score)
            beta = min(beta, minimum_score)
            if beta <= alpha:
                break
        return minimum_score

    def __str__(self):
        return "Alpha-Beta Minimax Agent"
