from typing import Tuple, Optional
from client.model.ai import AI
from client.model.player import Player
from client.model.game import Game
from client.model.abstract_rule import AbstractRule
from client.model.user import User
from client.model.account import Account


class GameManager:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        main_user: User,
        p1_account: Optional[Account],
        p2_account: Optional[Account],
        p1_first_move: bool = True,
        save: bool = False,
    ) -> None:
        """
        Initializes a game with the given parameters.
        :param player1 is the player that gets to play first
        :param player2 is the player that gets to play second
        :param main_user is the player1 user
        """
        self.__players: Tuple[Player, Player] = (player1, player2)
        self.main_user: User = main_user
        self.__board_size: int = self.main_user.get_preference().get_board_size()
        self.__rules: AbstractRule = self.main_user.get_preference().get_rule()
        self.game: Game = Game(
            board_size=self.__board_size,
            rules=self.__rules,
            p1_first_move=p1_first_move,
            save=save,
        )
        self._p1_account: Optional[Account] = p1_account
        self._p2_account: Optional[Account] = p2_account

    def make_move(self) -> None:
        self.__players[self.game.get_curr_player() - 1].place_tile(self.game)
        while isinstance(self.__players[self.game.get_curr_player() - 1], AI):
            self.__players[self.game.get_curr_player() - 1].place_tile(self.game)

    # def set_move(self, posn: Tuple[int, int]) -> None:
    #
    #     current_player: Player = self.get_player1()
    #     waiting_player: Player = self.get_player1()
    #     if self.game.get_curr_player() == 1:
    #         current_player: Player = self.get_player1()
    #         waiting_player: Player = (
    #             self.get_player2()
    #         )  # Used for "online opponent" reasons
    #     else:
    #         current_player: Player = self.get_player2()
    #         waiting_player: Player = (
    #             self.get_player1()
    #         )  # Used for "online opponent" reasons
    #
    #     if current_player.get_player_type() == "local_multi":
    #         current_player.set_next_move(posn=posn)
    #         current_player.place_tile(game=self.game)
    #     elif current_player.get_player_type() == "online":
    #         if current_player.get_user() == self.main_user:
    #             current_player.set_next_move(posn=posn)
    #             current_player.place_tile(game=self.game)
    #         else:
    #             # opponent is an online opponent, main_user cannot affect their movements:
    #             waiting_player.set_next_move(posn=posn)
    #     elif current_player.get_player_type() == "local_ai":
    #         current_player.g
    #         current_player.set_next_move()
    #     else:
    #         raise Exception("You cannot set the move for an AI in the parent class.")

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
