from typing import Tuple
from client.model.ai import AI
from client.model.player import Player
from client.model.game import Game
from client.model.abstract_rule import AbstractRule
from client.model.user import User


class GameManager:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        board_size: int,
        rules: AbstractRule,
        main_user: User,
    ) -> None:
        """
        Initializes a game with the given parameters.
        :param player1 is the player that gets to play first
        :param player2 is the player that gets to play second
        :param board_size is the size of the board based on the main user's preferences
        """
        self.__players: Tuple[Player, Player] = (player1, player2)
        self.__board_size: int = board_size
        self.__rules: AbstractRule = rules
        self.game: Game = Game(board_size=board_size, rules=rules)
        self.main_user: User = main_user

    def make_move(self) -> None:
        self.__players[self.game.get_curr_player() - 1].placeTile()
        while isinstance(self.__players[self.game.get_curr_player() - 1], AI):
            self.__players[self.game.get_curr_player() - 1].placeTile()

    def set_move(self, posn: Tuple[int, int]) -> None:
        if self.game.get_curr_player() == 1:
            current_player: Player = self.get_player1()
            waiting_player: Player = (
                self.get_player2()
            )  # Used for "online opponent" reasons
        else:
            current_player: Player = self.get_player2()
            waiting_player: Player = (
                self.get_player1()
            )  # Used for "online opponent" reasons

        if current_player.get_player_type() == "local_multi":
            current_player.set_next_move(posn=posn)
            current_player.place_tile(game=self.game)
        elif current_player.get_player_type() == "online":
            if current_player.get_user() == self.main_user:
                current_player.set_next_move(posn=posn)
                current_player.place_tile(game=self.game)
            else:
                # opponent is an online opponent, main_user cannot affect their movements:
                waiting_player.set_next_move(posn=posn)
        else:
            raise Exception("You cannot set the move for an AI in the parent class.")

    def get_player1(self) -> Player:
        """
        Get information about player 1
        :return: Player 1
        """
        return self.__players[0]

    def get_player2(self) -> Player:
        """
        Get information about player 2
        :return: Player 2
        """
        return self.__players[1]

    def get_rules(self) -> AbstractRule:
        """
        Get the current rules of the game
        :return: Rule that is being played in the game
        """
        return self.__rules
