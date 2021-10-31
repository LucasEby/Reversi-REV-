from typing import List, Tuple

from client.model.board import Board
from client.model.cell import CellState
from client.model.player import Player


class Game:
    def __init__(self, user1: User, user2: User, first_move: bool) -> None:
        self.id: int = id(self)
        # get the player who makes the first move from first_move (1 for user1, 0 for user2), this user will be player1
        # use the size and rule preference of this person, since both users must use the same size and rules
        if first_move:
            self.player1: Player = Player(user1, 1)
            self.player2: Player = Player(user2, 2)
            self.board: Board = Board(user1.get_preference().get_board_size(), 1)
            self.rules: ARules = user1.get_preference().get_rule()
        else:
            self.player1: Player = Player(user2, 1)
            self.player2: Player = Player(user1, 2)
            self.board: Board = Board(user2.get_preference().get_board_size(), 1)
            self.rules: ARules = user2.get_preference().get_rule()
        self.curr_player: int = 1
        self.save: bool = True

    # implement another constructor for playing vs AI (one user provided)
    # def __int__(self, user: User):

    def is_game_over(self) -> bool:
        """
        Check if the board has no empty spaces, no player1 disks, or no player2 disks.
        These are the states in which the game ends.

        :return: true if the game is over (no more turns can be made by one or both players), otherwise false
        """
        return (
            (self.board.get_num_type(CellState.empty) == 0)
            or (self.board.get_num_type(CellState.player1) == 0)
            or (self.board.get_num_type(CellState.player2) == 0)
        )

    def place_tile(self, posn: Tuple[int, int]) -> bool:
        """
        Place a tile on the given position of the board for the currently active player
        if the position is on the board and the move is valid according to the rules.

        :param posn: the position on the board to place a disk
        :raises Exception: Thrown when the given position is not on the board
        :return: True if the move was successfully completed, or false if it was invalid
        """
        if not self.is_valid_posn(posn[0], posn[1]):
            raise Exception("out-of bounds move attempted")
        if not self.rules.isValidMove(self.curr_player, posn, self.board):
            return False
        self.board.cells[posn[0]][posn[1]].fill(self.curr_player)
        # flip all Cells that are between this posn and any other curr_player disks
        self.__flip_opponents_tiles(posn)
        self.curr_player = 2 if self.curr_player == 1 else 1
        return True

    def is_valid_posn(self, x: int, y: int) -> bool:
        return (x in range(self.board.size)) and (y in range(self.board.size))

    def __flip_opponents_tiles(self, posn: Tuple[int, int]) -> None:
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
            if self.is_valid_posn(x, y) and (
                not self.board.cells[x][y].state.value
                in List[CellState.empty.value, self.curr_player]
            ):
                # iterate through all cells on the board in this direction that are filled with opponent's disk
                while self.is_valid_posn(x, y) and (
                    not self.board.cells[x][y].state.value
                    in List[CellState.empty.value, self.curr_player]
                ):
                    x += x_offset
                    y += y_offset
                # if the adjacent cell is not on the board, skip to next offset direction
                if not self.is_valid_posn(x, y):
                    continue
                # if we have found another curr_player disk, move backwards toward original posn,
                # flipping opponent disks as we go
                if self.board.cells[x][y].state.value == self.curr_player:
                    while (x, y) != posn:
                        x -= x_offset
                        y -= y_offset
                        self.board.cells[x][y].flip()

    def get_valid_moves(self) -> List[List[bool]]:
        """
        Get a board sized 2-D array of booleans. The boolean values represent whether a move on
        the board at that position is valid for the currently active player.

        :return: a 2-D array of booleans representing the locations of valid moves for the current player
        """
        valid_moves: List[List[bool]]
        for i in range(self.board.size):
            for j in range(self.board.size):
                valid_moves[i][j] = self.rules.isValidMove(
                    self.curr_player, (i, j), self.board
                )
        return valid_moves

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

    # def forfeit(self):
