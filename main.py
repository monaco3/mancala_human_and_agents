# from kalaha.controller import Controller
#
# if __name__ == '__main__':
#     N_COLS = 6
#     controller = Controller(N_COLS)
#     controller.play()

from kalaha.controller import Controller
from kalaha.minimax_agent import MinimaxAgent
from kalaha.alpha_beta import AlphaBetaMinimaxAgent
from kalaha.mctsAgent import MCTSAgent
from kalaha.RandomAgent import RandomAgent

from kalaha.gamex import Player

if __name__ == '__main__':
    N_COLS = 6
    agents = {
        Player.TOP:AlphaBetaMinimaxAgent(),
        Player.BOTTOM:MinimaxAgent()
    }
    controller = Controller(N_COLS, agents)
    controller.play()
