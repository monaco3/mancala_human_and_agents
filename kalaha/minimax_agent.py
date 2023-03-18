import copy

from kalaha.agent import Agent
from kalaha.player import Player


class MinimaxAgent(Agent):

    def __init__(self):
        self.max_depth = 2
    """
    An human agent providing a CLI to choose the moves
    """

    def choose(self, input_game) -> int:
        minimax = self.minimax(copy.deepcopy(input_game), 0)
        print(self.__str__(), "player chooses:", minimax)
        return minimax

    def minimax(self, input_game, depth: int) -> int:

        best_move = -1

        game = copy.deepcopy(input_game)

        # the top player wants to maximize the score of the board
        if game.current_player == Player.TOP:
            maximum_score = -48
            for i in game.get_possible_moves():
                game_copy = copy.deepcopy(game)
                game_copy.move_marbles(i)

                # if the player after the move is the top player again, then the scored should be maximized
                if game_copy.current_player == Player.TOP:
                    score = self.maximize(game_copy, depth + 1)
                    if score > maximum_score:
                        maximum_score = score
                        best_move = i

                elif game_copy.current_player == Player.BOTTOM:
                    score = self.minimize(game_copy, depth + 1)
                    if score > maximum_score:
                        maximum_score = score
                        best_move = i

        elif game.current_player == Player.BOTTOM:
            minimum_score = 48
            for i in game.get_possible_moves():
                game_copy = copy.deepcopy(game)
                game_copy.move_marbles(i)

                if game_copy.current_player == Player.TOP:
                    score = self.maximize(game_copy, depth + 1)
                    if score < minimum_score:
                        minimum_score = score
                        best_move = i

                if game_copy.current_player == Player.BOTTOM:
                    score = self.minimize(game_copy, depth + 1)
                    if score < minimum_score:
                        minimum_score = score
                        best_move = i

        return best_move

    def minimize(self, input_game, depth: int) -> int:
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
                score = self.minimize(game_copy, depth + 1)
            else:
                score = self.maximize(game_copy, depth + 1)
            if score < minimum_score:
                minimum_score = score
        return minimum_score

    def maximize(self, input_game, depth: int) -> int:
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
                score = self.minimize(game_copy, depth + 1)
            else:
                score = self.maximize(game_copy, depth + 1)
            if score > maximum_score:
                maximum_score = score
        return maximum_score

    def __str__(self):
        return "Minimax Agent"
