from typing import List, Tuple, Optional

from client.model.abstract_rule import AbstractRule
from client.model.board import Board
from client.model.cell import CellState
from client.model.player import Player
from client.model.user import User


class Game:
    def __init__(
        self, user1: User, user2: User, p1_first_move: bool = True, save: bool = False
    ) -> None:
        """
        Initializes a game with the given parameters
        :param user1: User correlating to player 1 (playing first)
        :param user2: User correlating to player 2 (playing second)
        :param p1_first_move: True if user1 has first move, false if user2 has first move
        :param save: Whether to save game after every turn
        """
        self._id: Optional[int] = None
        self._player1: Player = Player(1, user1)
        self._player2: Player = Player(2, user2)
        active_user: User = user1 if p1_first_move else user2
        # Use the size and rule preference of active user, since both users must use the same size and rules
        self.board: Board = Board(active_user.get_preference().get_board_size(), 1)
        self._rules: AbstractRule = active_user.get_preference().get_rule()
        self.save: bool = save
        self.curr_player: int = 1

    def is_game_over(self) -> bool:
        """
        Check if the board has no empty spaces, no player1 disks, no player2 disks, or current player has no valid moves
        These are the states in which the game ends.
        If current player has no valid moves, then no valid moves exist for either player since turn would
        have been ceded to opponent already.

        :return: true if the game is over (no more turns can be made by one or both players), otherwise false
        """
        return (
            (self.board.get_num_type(CellState.empty) == 0)
            or (self.board.get_num_type(CellState.player1) == 0)
            or (self.board.get_num_type(CellState.player2) == 0)
            or (not self.valid_moves_exist())
        )

    def place_tile(self, posn: Tuple[int, int]) -> bool:
        """
        Place a tile on the given position of the board for the currently active player
        if the position is on the board and the move is valid according to the rules.

        :param posn: the position on the board to place a disk
        :raises Exception: Thrown when the given position is not on the board
        :return: True if the move was successfully completed, or false if it was invalid
        """
        if not self.board.is_valid_posn(posn[0], posn[1]):
            raise Exception("out-of bounds move attempted")
        if not self._rules.is_valid_move(self.curr_player, posn, self.board):
            return False
        self.board.cells[posn[0]][posn[1]].fill(self.curr_player)

        # Flip all Cells that are between this posn and any other curr_player disks
        self.__flip_opponents_tiles(posn)

        # Set next player if they have a valid move
        self.curr_player = 2 if self.curr_player == 1 else 1
        if not self.valid_moves_exist():
            self.curr_player = 2 if self.curr_player == 1 else 1
        return True

    def __flip_opponents_tiles(self, posn: Tuple[int, int]) -> None:
        """
        Check for opponent disks around the given Tuple and flip any opponent cells that are between the given Tuple
        and any other curr_player disks.

        :param posn: the curr_player disk that may cause opponent tiles to be flipped
        """
        # check every cell around posn
        for x_offset, y_offset in (
            [1, 1],
            [1, -1],
            [-1, 1],
            [-1, -1],
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
        ):
            x, y = posn
            x += x_offset
            y += y_offset
            # make sure the cell is on the board and is filled with opponent's disk
            if self.board.is_valid_posn(x, y) and not (
                self.board.cells[x][y].state.value
                in [CellState.empty.value, self.curr_player]
            ):
                # Iterate through all cells on the board in this direction that are filled with opponent's disk
                while self.board.is_valid_posn(x, y) and not (
                    self.board.cells[x][y].state.value
                    in [CellState.empty.value, self.curr_player]
                ):
                    x += x_offset
                    y += y_offset
                # if the adjacent cell is not on the board, skip to next offset direction
                if not self.board.is_valid_posn(x, y):
                    continue
                # If we have found another curr_player disk, move backwards toward original posn,
                # flipping opponent disks as we go
                if self.board.cells[x][y].state.value == self.curr_player:
                    # Move back once at beginning
                    x -= x_offset
                    y -= y_offset
                    while (x, y) != posn:
                        self.board.cells[x][y].flip()
                        x -= x_offset
                        y -= y_offset

    def get_valid_moves(self) -> List[List[bool]]:
        """
        Get a board sized 2-D array of booleans. The boolean values represent whether a move on
        the board at that position is valid for the currently active player.

        :return: a 2-D array of booleans representing the locations of valid moves for the current player
        """
        valid_moves: List[List[bool]] = [
            [False for _ in range(self.board.size)] for _ in range(self.board.size)
        ]
        for i in range(self.board.size):
            for j in range(self.board.size):
                valid_moves[i][j] = self._rules.is_valid_move(
                    self.curr_player, (i, j), self.board
                )
        return valid_moves

    def valid_moves_exist(self) -> bool:
        """
        Return whether any valid moves exist for the active player
        :return: Moves exist (true) or not (false)
        """
        return any(
            [any([cell is True for cell in row]) for row in self.get_valid_moves()]
        )

    def get_winner(self) -> int:
        """
        Get the int representing the player who has more disks on the board.
        (1 for player1, 2 for player2)

        :raises Exception: Thrown when the method is called before the game has ended
        :return: the number representing the winning player
        """
        if not self.is_game_over():
            raise Exception("cannot get winner until game is over")
        if self.board.get_num_type(CellState.player1) > self.board.get_num_type(
            CellState.player2
        ):
            return 1
        else:
            return 2

    def get_score(self) -> Tuple[int, int]:
        """
        Get the scores for each player.

        :return: a tuple containing the scores for the two respective players
        """
        return self.board.get_num_type(CellState.player1), self.board.get_num_type(
            CellState.player2
        )

    def get_rules(self) -> AbstractRule:
        """
        Get the current rules of the game
        :return: Rule that is being played in the game
        """
        return self._rules

    def get_player1(self) -> Optional[Player]:
        """
        Get information about player 1
        :return: Player 1
        """
        return self._player1

    def get_player2(self) -> Optional[Player]:
        """
        Get information about player 2
        :return: Player 2
        """
        return self._player2

    def get_id(self) -> Optional[int]:
        """
        Returns ID of game
        : return: ID of game
        """
        return self._id

    def set_id(self, id: int) -> None:
        """
        Sets the ID of the game
        :param id: ID of the game
        """
        self._id = id

    def get_curr_player(self) -> int:
        """
        Returns the current player (next to play)
        :return: Next player as an integer
        """
        return self.curr_player

    # def forfeit(self):
