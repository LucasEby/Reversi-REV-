from abstract_rules import AbstractRules
from typing import Tuple, List
from client.model.board import Board


class Standard_Rules_2(AbstractRules):
    def __opponent_state(plyr_num: int):
        """
        finds the opposite player number given the current player number


        :param plyr_num: the current player's number state
        :raises error: None
        :return: int state
        """
        if plyr_num == 1:
            return 2
        elif plyr_num == 2:
            return 1
        else:
            # throw an error
            pass

    # """
    def __check_horizontal(brd: Board, posn: Tuple[int, int], plyr_num: int):
        """
        check to see if a valid move exists on the hoizontal with the chosen cell

        :param plyr_num: the current player's number state
        :param brd: current board state
        :param posn: tuple of the cell in question
        :raises error: None
        :return: bool, is it valid in the horizontal dimension
        """
        target_x = posn[0]
        target_y = posn[1]
        opp_num = __opponent_state(plyr_num)
        if (target_x > 1) and (target_x < len(brd) - 2):

            # Checking to the left here
            if target_x > 1:

                left_cells = []
                # list that holds all the cells to the left of the target

                # \/ Populate list of cells that are to the left of the target
                for lft_cll in range(0, target_x):
                    left_cells = left_cells + brd[lft_cll, target_y]

                if (opp_num in left_cells) and (plyr_num in left_cells):
                    opp_pos = 0
                    # nearest opponent cell position
                    friend_pos = 0
                    # nearest friendly cell position
                    search_pos = 0
                    # current position being checked

                    # loop over the list of cells to left
                    for c in reversed(left_cells):
                        # if the cell is a friendly cell update the friends cell position
                        if c == plyr_num:
                            friend_pos = search_pos
                        # if the cell is an opponent cell update the opponent cell position
                        elif c == opp_num:
                            opp_pos = search_pos
                        # update the search position once searching is done
                        search_pos += 1
                        # Check if an opponent exists to the left of the target and that a friendly exists to the left of that opponent
                        if opp_pos > 0 and friend_pos > opp_pos:
                            return True

            # Checking to the right here
            elif target_x < len(brd) - 2:
                right_cells = []
                # list that holds all the cells to the right of the target

                # \/ Populate list of cells that are to the right of the target
                for rght_cell in range(target_x, brd.len):
                    right_cells = right_cells + brd[rght_cell, target_y]

                if (opp_num in right_cells) and (plyr_num in right_cells):
                    opp_pos = 0
                    # nearest opponent cell position
                    friend_pos = 0
                    # nearest friendly cell position
                    search_pos = 0
                    # current position being checked
                    for c in right_cells:
                        # if the cell is a friendly cell update the friends cell position
                        if c == plyr_num:
                            friend_pos = search_pos
                        # if the cell is an opponent cell update the opponent cell position
                        elif c == opp_num:
                            opp_pos = search_pos
                        # update the search position once searching is done
                        search_pos += 1
                        # Check if an opponent exists to the right of the target and a friendly exists to the right of that opponent
                        if opp_pos > target_x and friend_pos > opp_pos:
                            return True
        else:
            return False

    def __check_vertical(brd: Board, posn: Tuple[int, int], plyr_num: int):
        """
        determines if a move is valid by checking the tiles in the same column as the target

        :param plyr_num: the current player's number state
        :param brd: current board state
        :param posn: potential position tuple
        :raises error: None
        :return: bool Is this a valid move?
        """
        target_x = posn[0]
        target_y = posn[1]
        opp_num = __opponent_state(plyr_num)

        if (target_y > 1) and (target_y < len(brd) - 2):

            # Checking above here
            if target_y > 1:

                above_cells = []
                # list that holds all the cells above the target

                # \/ Populate list of cells that are to the left of the target
                for abv_cll in range(0, target_y):
                    above_cells = above_cells + brd[target_x, abv_cll]

                if (opp_num in above_cells) and (plyr_num in above_cells):
                    opp_pos = 0
                    # nearest opponent cell position
                    friend_pos = 0
                    # nearest friendly cell position
                    search_pos = 0
                    # current position being checked

                    # loop over the list of cells to left
                    for c in above_cells:
                        # if the cell is a friendly cell update the friends cell position
                        if c == plyr_num:
                            friend_pos = search_pos
                        # if the cell is an opponent cell update the opponent cell position
                        elif c == opp_num:
                            opp_pos = search_pos
                        # update the search position once searching is done
                        search_pos += 1
                        # Check if an opponent exists to the left of the target and that a friendly exists to the left of that opponent
                        if opp_pos < len(above_cells) and friend_pos < opp_pos:
                            return True

            # Checking below here
            if target_y < len(brd) - 2:

                below_cells = []
                # list that holds all the cells above the target

                # \/ Populate list of cells that are to the left of the target
                for blw_cll in range(target_y, len(brd)):
                    below_cells = below_cells + brd[target_x, blw_cll]

                if (opp_num in below_cells) and (plyr_num in below_cells):
                    opp_pos = 0
                    # nearest opponent cell position
                    friend_pos = 0
                    # nearest friendly cell position
                    search_pos = 0
                    # current position being checked

                    # loop over the list of cells to left
                    for c in below_cells:
                        # if the cell is a friendly cell update the friends cell position
                        if c == plyr_num:
                            friend_pos = search_pos
                        # if the cell is an opponent cell update the opponent cell position
                        elif c == opp_num:
                            opp_pos = search_pos
                        # update the search position once searching is done
                        search_pos += 1
                        # Check if an opponent exists to the left of the target and that a friendly exists to the left of that opponent
                        if opp_pos > target_y and friend_pos > opp_pos:
                            return True

        return False

    def __check_diagonal(brd: Board, posn: Tuple[int, int], plyr_num: int):
        """
        deteremines whether or not a move is valid based on the position of tiles located along the diagonal


        :param plyr_num: the current player's number state
        :param brd: current board state
        :param posn: potential position tuple
        :raises error: None
        :return: bool Is this a valid move?
        """
        # check up and left, increase row, decrease column
        target_x: int = posn[0]
        target_y = posn[1]
        opp_num = __opponent_state(plyr_num)

        # Check Up-Right
        if (target_x < len(brd) - 2) and (target_y > 1):
            # not too close to the top right corner
            up_right_cells = []
            # list that holds all the cells up and to the right of the target

            # \/ Populate list of cells that are to the left of the target
            dim = [len(brd) - target_x, target_y]
            smallest_dim = min(dim)
            # need to ensure we dont get an index out of bounds error
            for i in range(smallest_dim):
                if i != 0:
                    up_right_cells = up_right_cells + brd[target_x + i, target_y - i]

            if (opp_num in up_right_cells) and (plyr_num in up_right_cells):
                opp_pos = 0
                # nearest opponent cell position
                friend_pos = 0
                # nearest friendly cell position
                search_pos = 0
                # current position being checked

                # loop over the list of cells to left
                for c in up_right_cells:
                    # if the cell is a friendly cell update the friends cell position
                    if c == plyr_num:
                        friend_pos = search_pos
                    # if the cell is an opponent cell update the opponent cell position
                    elif c == opp_num:
                        opp_pos = search_pos
                    # update the search position once searching is done
                    search_pos += 1
                    # Check if an opponent exists to the left of the target and that a friendly exists to the left of that opponent
                    if opp_pos > 0 and friend_pos > opp_pos:
                        return True

        # Check Down-Left
        if (target_x > 1) and (target_y < len(brd) - 2):
            # not too close to the bottom left corner
            bot_left_cells = []
            # list that holds all the cells down and to the left of the target
            dim = [target_x, len(brd) - target_y]
            smallest_dim = min(dim)
            # need to ensure we dont get an index out of bounds error
            for i in range(smallest_dim):
                if i != 0:
                    bot_left_cells = bot_left_cells + brd[target_x - i, target_y + i]

            if (opp_num in bot_left_cells) and (plyr_num in bot_left_cells):
                opp_pos = 0
                # nearest opponent cell position
                friend_pos = 0
                # nearest friendly cell position
                search_pos = 0
                # current position being checked

                # loop over the list of cells to left
                for c in bot_left_cells:
                    # if the cell is a friendly cell update the friends cell position
                    if c == plyr_num:
                        friend_pos = search_pos
                    # if the cell is an opponent cell update the opponent cell position
                    elif c == opp_num:
                        opp_pos = search_pos
                    # update the search position once searching is done
                    search_pos += 1
                    # Check if an opponent exists to the left of the target and that a friendly exists to the left of that opponent
                    if opp_pos > 0 and friend_pos > opp_pos:
                        return True

        # Check Up-Left
        if (target_x > 1) and (target_y > 1):
            # not too close to the top left corner
            top_left_cells = []
            # list that holds all the cells down and to the left of the target
            dim = [target_x, target_y]
            smallest_dim = min(dim)
            # need to ensure we dont get an index out of bounds error
            for i in range(smallest_dim):
                if i != 0:
                    top_left_cells = top_left_cells + brd[target_x - i, target_y - i]

            if (opp_num in top_left_cells) and (plyr_num in top_left_cells):
                opp_pos = 0
                # nearest opponent cell position
                friend_pos = 0
                # nearest friendly cell position
                search_pos = 0
                # current position being checked

                # loop over the list of cells to left
                for c in top_left_cells:
                    # if the cell is a friendly cell update the friends cell position
                    if c == plyr_num:
                        friend_pos = search_pos
                    # if the cell is an opponent cell update the opponent cell position
                    elif c == opp_num:
                        opp_pos = search_pos
                    # update the search position once searching is done
                    search_pos += 1
                    # Check if an opponent exists to the left of the target and that a friendly exists to the left of that opponent
                    if opp_pos > 0 and friend_pos > opp_pos:
                        return True

        # Check Down-Right
        if ((target_x < len(brd) - 2)) and (target_y < len(brd) - 2):
            # not too close to the top left corner
            bot_right_cells = []
            # list that holds all the cells down and to the left of the target
            dim = [target_x, target_y]
            smallest_dim = min(dim)
            # need to ensure we dont get an index out of bounds error
            for i in range(smallest_dim):
                if i != 0:
                    bot_right_cells = bot_right_cells + brd[target_x + i, target_y + i]

            if (opp_num in bot_right_cells) and (plyr_num in bot_right_cells):
                opp_pos = 0
                # nearest opponent cell position
                friend_pos = 0
                # nearest friendly cell position
                search_pos = 0
                # current position being checked

                # loop over the list of cells to left
                for c in bot_right_cells:
                    # if the cell is a friendly cell update the friends cell position
                    if c == plyr_num:
                        friend_pos = search_pos
                    # if the cell is an opponent cell update the opponent cell position
                    elif c == opp_num:
                        opp_pos = search_pos
                    # update the search position once searching is done
                    search_pos += 1
                    # Check if an opponent exists to the left of the target and that a friendly exists to the left of that opponent
                    if opp_pos > 0 and friend_pos > opp_pos:
                        return True

        return False

    def __is_valid_move(plyr_num: int, posn: Tuple[int, int], brd: Board):
        """
        determines if a move that was played is valid based on a given ruleset

        :param ply_num:the number of players in the game
        :param brd: current board state
        :param posn: potential position tuple
        :raises error: None
        :return: bool Is this a valid move?
        """
        # "must place a disk in such a position that there exists at least one straight (hoirzontal
        # vertical or diagonal) line between the new disk and any of her disks"
        is_valid_huh: bool = False
        # run some code here

        is_valid_huh = (
            __check_vertical(brd, posn, plyr_num)
            or __check_horizontal(brd, posn, plyr_num)
            or __check__diagonal((brd, posn, plyr_num))
        )

        return is_valid_huh
