from enum import Enum
import string


class GameView:

    __ABC_ARRAY = list(string.ascii_lowercase)

    def __init__(self, board_obj):
        """
        Fills in the needed board variables and initializes the current state of the board.

        :param board_obj: The specific board object the print_board method prints the state of.
        """
        self.__board = ""
        self.__board_obj = board_obj
        self.__size = board_obj.size
        self.print_board()

    def print_board(self):
        """
        Prints out the current state of the board.

        In the for loops, row and col loop from 0 to size [0, size] even though the column numbers and row numbers
        go from 0 to 1 - size [0, size). This was done on purpose to make space for the row numbers
        and column letters:
        """
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
                            self.__board_obj.getState(row, col) == "DiskP1"
                        ):  # [row][col]):
                            self.__board = self.__board + "  P1"
                        elif self.__board_obj.getState(row, col) == "DiskP2":
                            self.__board = self.__board + "  P2"
                        elif self.__board_obj.getState(row, col) == "Invalid":
                            print(
                                "Cell State was Invalid. Error in __constructBoard function of GameView"
                            )
                        elif self.__board_obj.getState(row, col) == "Empty":
                            self.__board = self.__board + "  __"
                if col == self.__size - 1:
                    self.__board = self.__board + "\n"
        print(self.__board)

    def print_winner(self):
        """
        Prints out the winner of the game.
        """
        print("Player " + self.__board_obj.get_winner() + " won the game!")

    def print_score(self):
        """
        Prints out the game's score.
        """
        temp_tuple = self.__board_ob.getscore()
        print("Player 1's score: " + temp_tuple[0])
        print("Player 2's score: " + temp_tuple[1])


# class Board:
#     def __init__(self, rowSize, colSize, nextTurn):
#         self.nextTurn = nextTurn  # nextTurn int
#         self.rowSize = rowSize  # Number of board rows
#         self.colSize = colSize  # Number of board columns
#         # Board starts out as being empty:
#         # member = Cell.Invalid
#         # tempRowList = [Cell(False).Invalid for i in range(colSize)]
#         member = Cell.DiskP1  # Enum('Cell', ['DiskP1', 'DiskP2', 'Empty', 'Invalid'])
#         tempRowList = [member for i in range(colSize)]
#         self.cells = [
#             list(tempRowList) for a in range(rowSize)
#         ]  # self.buildBoard() # cells: Cell[][]
#         self.__initializeBoard()
#
#     def __initializeBoard(self):
#         member = Cell.DiskP1
#         for row in range(0, self.rowSize):  #  loops from zero to 1 - rowSize
#             for col in range(0, self.colSize):  # loops from zero to 1 - colSize
#                 if row == 0:
#                     if col == 0:
#                         # member = Enum('Cell', ['DiskP1', 'DiskP2', 'Empty', 'Invalid'])
#                         # member.DiskP1.value = True
#                         # member.fill("DiskP1")  # Cell.Invalid)
#                         # self.cells[row][col] = member.fill("Invalid")# Cell.Invalid)
#                         self.cells[row][col] = member.fill("Invalid")
#                     else:  # col > 0:
#                         self.cells[row][col] = member.fill("Empty")
#                         # self.cells[row][col].fill("Empty")#Cell.Empty)
#                 else:  # row > 0
#                     if col == 0:
#                         self.cells[row][col] = member.fill("Invalid")
#                         # self.cells[row][col].fill("Invalid")#Cell.Invalid)
#                     else:
#                         self.cells[row][col] = member.fill("Empty")
#                         # self.cells[row][col].fill("Empty") #Cell.Empty)
#
#     # +getState(): Cell[][]:
#     def getState(self, row, column):
#         return self.cells[row][column].name
#         # if self.cells[row][column].name == "Invalid":
#         #     return self.cells[row][column].Invalid.name
#         # elif self.cells[row][column].DiskP1.value:
#         #     return self.cells[row][column].DiskP1.name
#         # elif self.cells[row][column].DiskP2.value:
#         #     return self.cells[row][column].DiskP2.name
#         # else:  # self.cells[row][column].Empty.value
#         #     return self.cells[row][column].Empty.name
#         # return self.cells[row][column]
#
#     # +getState(): Cell[][]:
#     # def getState(self, row, column):
#     #     member = self.cells[row][column]
#     #     if member.DiskP1:
#     #         return self.DiskP1
#     #
#     #     elif member.DiskP2:
#     #         return self.DiskP2
#     #
#     #     elif member.Empty:
#     #         return member.Empty
#     #
#     #     elif member.Invalid:
#     #         return self.cells[row][column].Invalid
#     #     else:
#     #         print("Error in __fill function of Cell")
#     #
#     #     return cell
#
#
# class Cell(Enum):
#     DiskP1 = 0  # False
#     DiskP2 = 1  # False
#     Empty = 2  # False
#     Invalid = 3  # False
#
#     # def __init__(self):
#     #     self.DiskP1 = False
#     #     self.DiskP2 = False
#     #     self.Empty = False
#     #     self.Invalid = False
#
#     # I didn't understand what the difference between flip and fill were so I just created fill:
#     def flip(self):  # +flip(): void
#         print("")
#
#     def fill(self, fillName):  # , member): # +fill(): void
#         if fillName == "DiskP1":
#             return Cell.DiskP1
#         if fillName == "DiskP2":
#             return Cell.DiskP2
#         if fillName == "Empty":
#             return Cell.Empty
#         if fillName == "Invalid":
#             return Cell.Invalid
#         # if fillName == "DiskP1":
#         # #if self.Name == "DiskP1":
#         #     member = Cell.DiskP1
#         #     member.value = True
#         #     return member
#         # elif self.Name == "DiskP2":
#         #     member = Cell.DiskP2
#         #     member.value = True
#         #     return member
#         # elif self.Name == "Empty":
#         #     member = Cell.Empty
#         #     member.value = True
#         #     return member
#         # elif self.Name == "Invalid":
#         #     member = Cell.Invalid
#         #     member.value = True
#         #     return member
#         ###########
#         #     self.DiskP1 = True
#         #     self.DiskP2 = False
#         #     self.Empty = False
#         #     self.Invalid = False
#         # elif self.Name == "DiskP2":
#         #     self.DiskP1 = False
#         #     self.DiskP2 = True
#         #     self.Empty = False
#         #     self.Invalid = False
#         # elif self.Name == "Empty":
#         #     self.DiskP1 = False
#         #     self.DiskP2 = False
#         #     self.Empty = True
#         #     self.Invalid = False
#         # elif self.Name == "Invalid":
#         #     self.DiskP1 = False
#         #     self.DiskP2 = False
#         #     self.Empty = False
#         #     self.Invalid = True
#         # else:
#         #     print("Error in __fill function of Cell")
#         ##############
#         # if self.Invalid == Cell.DiskP1.Invalid:
#         # if member.name == Cell.DiskP1.name:
#         #     self.DiskP1 = True
#         #     self.DiskP2 = False
#         #     self.Empty = False
#         #     self.Invalid = False
#         #
#         # elif member.name == Cell.DiskP2.name:
#         #     self.DiskP1 = False
#         #     self.DiskP2 = True
#         #     self.Empty = False
#         #     self.Invalid = False
#         #
#         # elif member.name == Cell.Empty.name:
#         #     self.DiskP1 = False
#         #     self.DiskP2 = False
#         #     self.Empty = True
#         #     self.Invalid = False
#         #
#         # elif member.name == Cell.Invalid.name:
#         #     self.DiskP1 = False
#         #     self.DiskP2 = False
#         #     self.Empty = False
#         #     self.Invalid = True
#         # else:
#         # print("Error in __fill function of Cell")
#
#
# # GameView Test:
# # member = Cell.Invalid #Cell()#Enum('Cell', ['DiskP1', 'DiskP2', 'Empty', 'Invalid'])
# obj = Board(6, 6, 1)
# viewObj = GameView(obj)
#
# # Other Random Tests:
# # member = Cell.Invalid #Cell()#Enum('Cell', ['DiskP1', 'DiskP2', 'Empty', 'Invalid'])
# # print(member)
# # member = Cell.Empty
# # print(member)
# # obj = Board(6, 6, 1)
# # print(obj.getState[6, 6])
# # print(obj.getState(3, 3))
# # print(obj.getState(0,0))
# # self.boardObj.getState(row, col).name == "DiskP1":
