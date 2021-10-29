import string


class GamePageView(BasePageView):

    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(self, game_obj: Game, board_obj: Board) -> None:
        """
        Fills in the needed board variables and initializes the current state of the board.

        :param board_obj: The specific board object the print_board method prints the state of.
        :param game_obj: A specific game object who's attributes will be accessed and printed.
        """
        self.__board = ""
        self.__game_obj = game_obj
        self.__board_obj = board_obj
        self.__size = board_obj.size
        self.__board_state = board_obj.get_state()

    def display(self) -> None:
        self.display_board()
        self.display_score()

    def display_board(self) -> None:
        """
        Prints out the current state of the board.

        In the for loops, row and col loop from 0 to size [0, size] even though the column numbers and row numbers
        go from 0 to 1 - size [0, size). This was done on purpose to make space for the row numbers
        and column letters:
        """
        self.__board = ""  # reset board string.
        for row in range(0, self.__size + 1):
            for col in range(0, self.__size + 1):
                if row == 0:
                    if col > 0:
                        self.__board = self.__board + "   " + self.__ABC_ARRAY[col - 1]
                else:  # row > 0
                    if col == 0:
                        self.__board = self.__board + str(row)
                    else:
                        if (
                            self.__board_state[row][col].state == "DiskP1"
                        ):  # [row][col]):
                            self.__board = self.__board + "  P1"
                        elif self.__board_state[row][col].state == "DiskP2":
                            self.__board = self.__board + "  P2"
                        elif self.__board_state[row][col].state == "Invalid":
                            print(
                                "Cell State was Invalid. Error in __constructBoard function of GameView"
                            )
                        elif self.__board_state[row][col].state == "Empty":
                            self.__board = self.__board + "  __"
                if col == self.__size - 1:
                    self.__board = self.__board + "\n"
        print(self.__board)

    def display_winner(self) -> None:
        """
        Prints out the winner of the game.
        """
        winner_string = str(self.__game_obj.get_winner())
        print("Player " + winner_string + " won the game!")

    def display_score(self) -> None:
        """
        Prints out the game's score.
        """
        temp_tuple = self.__game_obj.get_score()
        temp_string0 = str(temp_tuple[0])
        temp_string1 = str(temp_tuple[1])
        print("Player 1's score: " + temp_string0)
        print("Player 2's score: " + temp_string1)

    def update_game_and_board(self, game_obj: Game, board_obj: Board) -> None:
        """
        Updates the board and game objects.
        """
        self.__game_obj = game_obj
        self.__board_obj = board_obj
        self.__size = board_obj.size
        self.__board_state = board_obj.get_state()
