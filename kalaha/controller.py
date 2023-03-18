from kalaha.gamex import Kalaha, Player

class Controller:
    """
    The controller requests moves to the agents (whetever their are human or AI) and applies it to the game
    """
    #
    # def __init__(self, cols):
    #     self.cols = cols
    #     self.game = Kalaha(self.cols)

    def __init__(self, cols, agents):
        self.cols = cols
        self.game = Kalaha(self.cols, agents)

    def play(self) -> Player:
        """
        Starts a game with the two agent and manages it till the end
        Don't call this method twice, but create a new controller with two
        new agents (Agents could be stateful)
        """

        print(self.game.__str__())

        while self.game.winner == Player.BLANK:
            choice = self.game.agents[self.game.current_player].choose(self.game)
            if self.game.is_valid(choice):
                self.game.move_marbles(choice)
                print(self.game.__str__())
            else:
                print("That is not a valid choice, try again.")

        print(f"Player {self.game.winner.name} Won!")

        return self.game.winner
