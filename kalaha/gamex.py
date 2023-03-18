# class Player
# class Cup
# class Store
# class Move
# class Kalaha
import string
from typing import Dict, List, Tuple, Optional, Union, Iterable
from enum import Enum

from kalaha.agent import Agent
from kalaha.human_agent import HumanAgent
from kalaha.minimax_agent import MinimaxAgent
from kalaha.player import Player


class Cup:
    def __init__(self, player: Player, col: int, marbles: int):
        self.side = player
        self.col = col
        self.marbles = marbles


class Store(Cup):
    pass


# two lists of cups for a player, with pointer to next cup
# each cup says who the player it belongs to and the number of marbles in cup


class Kalaha:
    """
    The game state
    """

    def __init__(self, cols,agents):
        self.cols = cols
        self.agents = agents
        self.current_player: Player = Player.BOTTOM

        self.player_bottom: Agent = HumanAgent()
        self.player_top: Agent = MinimaxAgent()
        self.agents = {Player.BOTTOM: self.player_bottom, Player.TOP: self.player_top}

        self.sides = {
            Player.TOP: [Cup(Player.TOP, i, 4) for i in range(self.cols)],
            Player.BOTTOM: [Cup(Player.BOTTOM, i, 4) for i in range(self.cols)]
        }
        self.stores = {
            Player.TOP: Store(Player.TOP, 0, 0),
            Player.BOTTOM: Store(Player.BOTTOM, 0, 0)
        }
        self.winner = Player.BLANK

    def get_players_cups(self, player: Player) -> List[Cup]:
        return self.sides[player]

    def get_cup_by_id(self, player, number) -> Cup:
        return self.sides[player][number]

    def check_game(self):
        return self.winner != Player.BLANK

    def is_valid(self, choice: int):
        # check that the input choice is valid, can move that cell
        if choice < 0 or choice > 5:
            return False
        elif self.sides[self.current_player][choice].marbles <= 0:
            return False
        else:
            return True

    def did_steal(self, last):
        opp = self.current_player.opponent()
        # if the last cup a marble was placed in was empty then it takes opposing
        if last[0] == "turn":  # if lands on current player's side
            last_id = last[1]
            last_cup = self.get_cup_by_id(self.current_player, last_id)

            # get the opposing players cup
            opp_cup_id = self.cols - last_id - 1
            opp_cup: Cup = self.sides[opp][opp_cup_id]
            opp_marbles = opp_cup.marbles

            # if lands in empty cup and opposite cup is not empty
            if last_cup.marbles == 1 and opp_marbles > 0:
                # empty the last cup
                self.sides[self.current_player][last[1]] = Cup(
                    self.current_player, last_id, 0)
                # add the marbles to the store
                self.stores[self.current_player].marbles = self.stores[self.current_player].marbles + 1 + opp_marbles
                # empty the opponents cup
                self.sides[opp][opp_cup_id].marbles = 0
                return True

        else:
            return False

    def after_move(self, last):
        # check if any side has all empty
        # if so declare the winner
        player_top_marbles = sum(map(lambda c: c.marbles, self.sides[Player.TOP]))
        player_bottom_marbles = sum(map(lambda c: c.marbles, self.sides[Player.BOTTOM]))
        if player_top_marbles == 0:
            self.stores[Player.TOP].marbles = self.stores[Player.TOP].marbles + player_bottom_marbles
            self.winner = Player.TOP
        if player_bottom_marbles == 0:
            self.stores[Player.BOTTOM].marbles = self.stores[Player.BOTTOM].marbles + player_top_marbles
            self.winner = Player.BOTTOM

        self.current_player = self.current_player.opponent()

        # if the last cup was the store then goes again
        if last[0] == "store":
            self.current_player = self.current_player.opponent()
            # print("Last marble landed in your store. Go again!")

    def move_marbles(self, cup_id: int):
        # moves the marbles from cup_id and returns the last cup a marble is dropped
        # returns the tuple specifying what side/store it lands on, the cup number on that side

        # check if cup has marbles maybe
        # check if valid move?
        # empty the cup and add 1 to every following possible cup/store
        # start_cup = cup.get_col()
        start_cup = self.get_cup_by_id(self.current_player, cup_id)
        num_marbles = start_cup.marbles
        self.sides[self.current_player][cup_id].marbles = 0

        # more general turn
        opp = self.current_player.opponent()
        opp_count = 0
        curr = cup_id + 1
        last_cup = ("turn", curr)
        for i in range(cup_id + 1, cup_id + num_marbles + 1):
            if curr < self.cols or (i >= self.cols & opp_count >= self.cols):
                # if curr is greater than or equal to 6 and opp_count is greater than 6 too
                # means it already went around both sides and is back to self.turn's row
                # so set it back to first cup of turn and also opp to 0 in case it goes
                # back to the opposing turn's side
                if curr >= self.cols:
                    curr = 0
                    opp_count = 0
                self.sides[self.current_player][curr] = Cup(
                    self.current_player, curr, self.sides[self.current_player][curr].marbles + 1)
                last_cup = ("turn", curr)
                curr += 1
            elif i > self.cols:  # else it goes into top players side
                if opp_count < self.cols:
                    self.sides[opp][opp_count] = Cup(
                        opp, opp_count, self.sides[opp][opp_count].marbles + 1)
                    last_cup = ("opp", opp_count)
                    opp_count += 1
                else:  # go back to start of turn's row, not sure needed here anymore
                    # taken care of in first if
                    opp_count = 0
            else:  # else the cup col number is equal to the store
                if curr == self.cols:  # necessary if?
                    self.stores[self.current_player].marbles = self.stores[self.current_player].marbles + 1
                    last_cup = ("store", 0)
            # print(last_cup[0])
        self.did_steal(last_cup)
        self.after_move(last_cup)

        # in a post turn function, check if the whole side of a player is empty
        # then it's end of the game
        # in a post turn, if end marbles in store, that person goes again
        #  if last marble lands in an empty cup, that person takes the opposing cup too
        # need to revise steal, steals at the very end when there's just 1's moving around
        #    and should not be stealing

    def get_possible_moves(self):
        moves = []
        for i in self.sides[self.current_player]:
            if i.marbles != 0:
                moves.append(i.col)
        return moves

    def get_score(self):
        return self.stores[Player.TOP].marbles - self.stores[Player.BOTTOM].marbles

    def __str__(self):

        border = "--" * (self.cols * 2)
        row_separator = "  " + "--" * self.cols

        returned_string = "    5 4 3 2 1 0\n"
        returned_string = returned_string + border + "\n"

        top = "    "
        for cupt in reversed(self.sides[Player.TOP]):
            top += str(cupt.marbles) + " "
        returned_string = returned_string + top + "\n"
        stores = str(self.stores[Player.TOP].marbles) + \
                 row_separator + " " + str(self.stores[Player.BOTTOM].marbles)
        returned_string = returned_string + stores + "\n"
        bottom = "    "
        for cupb in self.sides[Player.BOTTOM]:
            bottom += str(cupb.marbles) + " "
        returned_string = returned_string + bottom + "\n"

        returned_string = returned_string + border + "\n"
        returned_string = returned_string + "    0 1 2 3 4 5\n"
        return returned_string + "\n"
