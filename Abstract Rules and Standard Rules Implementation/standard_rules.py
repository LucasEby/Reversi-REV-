from abstract_rules import AbstractRules
from typing import Tuple, List


class standard_rules(AbstractRules):
    def __opponent_state(plyr_num: int):
        """
        finds the opposite player number given the current player number
        """
        if( plyr_num == 1):
            return 2
        if(plyr_num == 2):
            return 1
        else:
            #throw an error
            pass
    #"""
    def __check_horizontal_2(brd: Board, posn: Tuple[int, int],plyr_num: int):
        target_x = posn[0]
        target_y = posn[1]
        opp_num = __opponent_state(plyr_num)
        if ((posn[0] > 1) and  (posn[0] < len(brd)-2)):
            
            #Checking to the left here
            if (posn[0] > 1):
                
                left_cells = []
                #list that holds all the cells to the left of the target
                
                #\/ Populate list of cells that are to the left of the target 
                for lft_cll in range(0, target_x):
                    left_cells = left_cells + brd[lft_cll, target_y]
                
                if (opp_num in left_cells ) and (plyr_num in left_cells):
                    opp_pos = 0
                    #nearest opponent cell position
                    friend_pos = 0
                    #nearest friendly cell position
                    search_pos = 0
                    #current position being checked
                    
                    #loop over the list of cells to left 
                    for c in reversed(left_cells):
                        #if the cell is a friendly cell update the friends cell position
                        if c == plyr_num :
                            friend_pos = search_pos
                        #if the cell is an opponent cell update the opponent cell position
                        elif c == opp_num:
                            opp_pos = search_pos
                        #update the search position once searching is done
                        search_pos += 1
                        #Check if an opponent exists to the left of the target and that a friendly exists to the right of that opponent
                        if(opp_pos > 0 and friend_pos > opp_pos):
                            return True

            #Checking to the right here
            elif posn[0] < len(brd)-2:
                pass
        else:
            return False
    #"""

    def __check_horizontal(brd: Board, posn: Tuple[int, int],plyr_num: int):
        is_horizontal_huh: bool = False

        #cells: List[List[Cell]] list of list of cells, first list is the column, 2nd is the row
        #  |0 1 2 3  Cells[2][1]
        # 0|          posn[2][1]
        # 1|? ? X
        # 2|
        # 3|

        #check to the left
        # iterate from 0 to posn[0] if posn[0] > 2
        if(posn[0] > 1):
            i = 0
            for this_cell in brd.cells[posn[i]]:
                #first we gotta check to see if their is even is an opponent cell to the left of the selected cell
                if(cell.state == __opponent_state(plyr_num)):
                    #since there is an opponent we then check for a friendly cell to the left of the opposing cell
                    #for cell in brd.cells[???]:
                    # if all of this is true we have 1 valid layout and can return true
                    #return is_horizontal_huh, not sure which is better coding practice <- This or \/ that
                    return True
        
        #check to the right
        # position needs to be at least 3 away from the right edge of the board
        if(posn[0] < brd.cells[0].length - 2):
            #TODO: Do I have my rows and columns right?
            for cell in range(posn[0],brd.cells[0].length):
                #TODO: Does range work like I think it does?
                if(cell.state == __opponent_state(plyr_num)):
                    #there exists an opponent cell to the right of the current cell if we reach this line
                    for cll in range(cell[0],brd.cells[0].length):
                        #TODO: check range but needs to check to the right of the current cell from
                        #      the previous for loop
                        if(cll.state == plyr_num):
                            return True
        # wasnt a valid oreientation of tiles to the left or to the right
        return False
    
    def __check_vertical(brd: Board, posn: Tuple[int, int], plyr_num: int):
        is_vertical_huh:bool = False

        #check above
        #check below

        return is_vertical_huh
    
    def __check_diagonal(brd: Board, posn: Tuple[int, int], plyr_num: int):
        is_diagonal_huh:bool = False
        #check up and left, increase row, decrease column
        #check down and left, decrease row, decrease column
        #check up and right, increase column, increase row
        #check down and right, increase column, decrease row
        return is_diagonal_huh

    def __is_valid_move(plyr_num: int, posn: Tuple[int, int], brd: Board):
        """
        determines if a move that was played is valid based on a given ruleset

        :param ply_num:the number of players in the game
        :param posn: the position of the move that is being evaluated
        :raises error: None
        :return: Whether a move was valid, True, or not, False
        """
        #"must place a disk in such a position that there exists at least one straight (hoirzontal 
        # vertical or diagonal) line between the new disk and any of her disks"
        is_valid_huh: bool = False
        #run some code here

        is_valid_huh = __check_vertical(brd, posn, plyr_num) or __check_horizontal(brd, posn, plyr_num) or __check__diagonal((brd, posn, plyr_num))


        return is_valid_huh
