from board import *
from cell import *
from player import *


class Game:
    def __init__(self, user1: User, user2: User) -> None:
        self.id: int = id(self)
        self.board: Board = Board(user1.pref.board_size, 1)
        self.rules: ARules = user1.pref.rules
        self.player1: Player = Player(user1)
        self.player2: Player = Player(user2)
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
            (self.board.get_num_type(0) == 0)
            or (self.board.get_num_type(1) == 0)
            or (self.board.get_num_type(2) == 0)
        )

    def place_tile(self, posn: Tuple[int,int]) -> bool:
        """
        Place a tile on the given position of the board for the currently active player
        if the position is on the board and the move is valid according to the rules.

        :param posn: the position on the board to place a disk
        :raises Exception: Thrown when the given position is not on the board
        :return: True if the move was successfully completed, or false if it was invalid
        """
        if (
            (posn[0]
            < 0) or (posn[0]
            >= self.board.size) or (posn[1]
            < 0) or (posn[1]
            >= self.board.size)
        ):
            raise Exception("out-of bounds move attempted")
        if not self.rules.isValidMove(self.curr_player, posn, self.board):
            return False
        self.board.cells[posn[0]][posn[1]] = self.board.cells[posn[0]][posn[1]].fill(
            self.curr_player
        )
        self.curr_player = 2 if self.curr_player == 1 else 1
        return True

    def get_valid_moves(self): -> List[bool]:
        """
        Get a board sized 2-D array of booleans. The boolean values represent whether a move on
        the board at that position is valid for the currently active player.

        :return: a 2-D array of booleans representing the locations of valid moves for the current player
        """
        for i in self.board.size:
            for j in self.board.size:
                validMoves[i][j] = self.rules.isValidMove(self.curr_player, tuple(i, j), self.board)
        return validMoves

    def get_winner(self) -> int:
        """
        Get the int representing the player who has more disks on the board.
        (1 for player1, 2 for player2)

        :raises Exception: Thrown when the method is called before the game has ended
        :return: the number representing the winning player
        """
        if not self.is_game_over():
            raise Exception("cannot get winner until game is over")
        if self.board.get_num_type(1) > self.board.get_num_type(2):
            return 1
        else:
            return 2

    def get_score(self) -> Tuple[int,int]:
        """
        Get the scores for each player.

        :return: a tuple containing the scores for the two respective players
        """
        return tuple(self.board.get_num_type(1), self.board.get_num_type(2))

    # def forfeit(self):
