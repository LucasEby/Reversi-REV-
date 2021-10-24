from enum import Enum
import string


class GameView:

    abcArray = list(string.ascii_lowercase)

    def __init__(self, boardObj):
        self.board = ""
        self.boardObj = boardObj
        self.rowSize = boardObj.rowSize
        self.colSize = boardObj.colSize
        self.printBoard()

    def printBoard(self):
        for row in range(0, self.rowSize):  # loops from zero to 1 - rowSize
            for col in range(0, self.colSize):  # loops from zero to 1 - colSize
                if row == 0:
                    if col > 0:
                        self.board = (self.board + "   " + self.abcArray[col - 1])
                else:  # row > 0
                    if col == 0:
                        self.board = (self.board + str(row))
                    else:
                        if self.boardObj.getState(row, col) == "DiskP1": #[row][col]):
                            self.board = (self.board + "  P1")
                        elif self.boardObj.getState(row, col) == "DiskP2":
                            self.board = (self.board + "  P2")
                        elif self.boardObj.getState(row, col) == "Invalid":
                            print("Cell State was Invalid. Error in __constructBoard function of GameView")
                        elif self.boardObj.getState(row, col) == "Empty":
                            self.board = (self.board + "  __")
                if col == self.rowSize - 1:
                    self.board = self.board + "\n"
        print(self.board)


class Board:

    def __init__(self, rowSize, colSize, nextTurn):
        self.nextTurn = nextTurn  # nextTurn int
        self.rowSize = rowSize  # Number of board rows
        self.colSize = colSize  # Number of board columns
        # Board starts out as being empty:
        # member = Cell.Invalid
        #tempRowList = [Cell(False).Invalid for i in range(colSize)]
        member = Cell.DiskP1 #Enum('Cell', ['DiskP1', 'DiskP2', 'Empty', 'Invalid'])
        tempRowList = [member for i in range(colSize)]
        self.cells = [list(tempRowList) for a in range(rowSize)]  # self.buildBoard() # cells: Cell[][]
        self.__initializeBoard()

    def __initializeBoard(self):
        member = Cell.DiskP1
        for row in range(0, self.rowSize): #  loops from zero to 1 - rowSize
            for col in range(0, self.colSize):  # loops from zero to 1 - colSize
                if row == 0:
                    if col == 0:
                        # member = Enum('Cell', ['DiskP1', 'DiskP2', 'Empty', 'Invalid'])
                        # member.DiskP1.value = True
                        # member.fill("DiskP1")  # Cell.Invalid)
                        # self.cells[row][col] = member.fill("Invalid")# Cell.Invalid)
                        self.cells[row][col] = member.fill("Invalid")
                    else:  # col > 0:
                        self.cells[row][col] = member.fill("Empty")
                        #self.cells[row][col].fill("Empty")#Cell.Empty)
                else:  # row > 0
                    if col == 0:
                        self.cells[row][col] = member.fill("Invalid")
                        #self.cells[row][col].fill("Invalid")#Cell.Invalid)
                    else:
                        self.cells[row][col] = member.fill("Empty")
                        #self.cells[row][col].fill("Empty") #Cell.Empty)

    # +getState(): Cell[][]:
    def getState(self, row, column):
        return self.cells[row][column].name
        # if self.cells[row][column].name == "Invalid":
        #     return self.cells[row][column].Invalid.name
        # elif self.cells[row][column].DiskP1.value:
        #     return self.cells[row][column].DiskP1.name
        # elif self.cells[row][column].DiskP2.value:
        #     return self.cells[row][column].DiskP2.name
        # else:  # self.cells[row][column].Empty.value
        #     return self.cells[row][column].Empty.name
        # return self.cells[row][column]

    # +getState(): Cell[][]:
    # def getState(self, row, column):
    #     member = self.cells[row][column]
    #     if member.DiskP1:
    #         return self.DiskP1
    #
    #     elif member.DiskP2:
    #         return self.DiskP2
    #
    #     elif member.Empty:
    #         return member.Empty
    #
    #     elif member.Invalid:
    #         return self.cells[row][column].Invalid
    #     else:
    #         print("Error in __fill function of Cell")
    #
    #     return cell


class Cell(Enum):
    DiskP1 = 0 #False
    DiskP2 = 1 #False
    Empty = 2 #False
    Invalid = 3 #False

    # def __init__(self):
    #     self.DiskP1 = False
    #     self.DiskP2 = False
    #     self.Empty = False
    #     self.Invalid = False

    # I didn't understand what the difference between flip and fill were so I just created fill:
    def flip(self): # +flip(): void
        print("")

    def fill(self, fillName):  # , member): # +fill(): void
        if fillName == "DiskP1":
            return Cell.DiskP1
        if fillName == "DiskP2":
            return Cell.DiskP2
        if fillName == "Empty":
            return Cell.Empty
        if fillName == "Invalid":
            return Cell.Invalid
        # if fillName == "DiskP1":
        # #if self.Name == "DiskP1":
        #     member = Cell.DiskP1
        #     member.value = True
        #     return member
        # elif self.Name == "DiskP2":
        #     member = Cell.DiskP2
        #     member.value = True
        #     return member
        # elif self.Name == "Empty":
        #     member = Cell.Empty
        #     member.value = True
        #     return member
        # elif self.Name == "Invalid":
        #     member = Cell.Invalid
        #     member.value = True
        #     return member
        ###########
        #     self.DiskP1 = True
        #     self.DiskP2 = False
        #     self.Empty = False
        #     self.Invalid = False
        # elif self.Name == "DiskP2":
        #     self.DiskP1 = False
        #     self.DiskP2 = True
        #     self.Empty = False
        #     self.Invalid = False
        # elif self.Name == "Empty":
        #     self.DiskP1 = False
        #     self.DiskP2 = False
        #     self.Empty = True
        #     self.Invalid = False
        # elif self.Name == "Invalid":
        #     self.DiskP1 = False
        #     self.DiskP2 = False
        #     self.Empty = False
        #     self.Invalid = True
        # else:
        #     print("Error in __fill function of Cell")
        ##############
        # if self.Invalid == Cell.DiskP1.Invalid:
        # if member.name == Cell.DiskP1.name:
        #     self.DiskP1 = True
        #     self.DiskP2 = False
        #     self.Empty = False
        #     self.Invalid = False
        #
        # elif member.name == Cell.DiskP2.name:
        #     self.DiskP1 = False
        #     self.DiskP2 = True
        #     self.Empty = False
        #     self.Invalid = False
        #
        # elif member.name == Cell.Empty.name:
        #     self.DiskP1 = False
        #     self.DiskP2 = False
        #     self.Empty = True
        #     self.Invalid = False
        #
        # elif member.name == Cell.Invalid.name:
        #     self.DiskP1 = False
        #     self.DiskP2 = False
        #     self.Empty = False
        #     self.Invalid = True
        #else:
        #print("Error in __fill function of Cell")

#GameView Test:
#member = Cell.Invalid #Cell()#Enum('Cell', ['DiskP1', 'DiskP2', 'Empty', 'Invalid'])
obj = Board(6, 6, 1)
viewObj = GameView(obj)

#Other Random Tests:
#member = Cell.Invalid #Cell()#Enum('Cell', ['DiskP1', 'DiskP2', 'Empty', 'Invalid'])
#print(member)
#member = Cell.Empty
#print(member)
#obj = Board(6, 6, 1)
#print(obj.getState[6, 6])
#print(obj.getState(3, 3))
#print(obj.getState(0,0))
#self.boardObj.getState(row, col).name == "DiskP1":
