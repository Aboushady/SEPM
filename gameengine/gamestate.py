from .utils import *
from .move import Move


class GameState:
    """
        GameState as we have defined it. A 3-dimensional array with coordinates on form of (square, x ,y) with values that represent color of stone.
        Has attributes: board and number_of_moves_made
    """

    def __init__(self, black_stones=[], white_stones=[], number_of_moves_made=0):
        """
            Constructor of the game state: Initialize the game state according to the arguments provided.

            Args:
                 (List, 3x3x3 tuples) black_stones: Coordinates of all black stones
                (List, 3x3x3 tuples) white_stones: Coordinates of all white stones
                (Integer) number_of_moves_made: which round the game state is in
        """
        self.board = dict()
        self.number_of_moves_made = number_of_moves_made

        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if (not y == 1) or (not z == 1):
                        self.board[(x, y, z)] = BOARD_SLOT.empty
        for stone in black_stones:
            self.board[stone] = BOARD_SLOT.black
        for stone in white_stones:
            self.board[stone] = BOARD_SLOT.white

    def get_number_of_moves_made(self):
        """
            Gets the current move number, which always starts from 0.

            Returns:
                (Integer) Current move number.
        """
        return self.number_of_moves_made

    def get_all_stone_positions(self):
        """
            Gets the positions of all the stones in the current game state and returns them in a list for each color.

            Returns:
                (List, 3x3x3 tuples) black_stones: Coordinates of all black stones
                (List, 3x3x3 tuples) white_stones: Coordinates of all white stones
        """
        black_stones = []
        white_stones = []

        for key, value in self.board.items():
            if value == BOARD_SLOT.black:
                black_stones.append(key)
            elif value == BOARD_SLOT.white:
                white_stones.append(key)

        return black_stones, white_stones

    def __str__(self):
        """
            Prints the current state of the game board as ASCII art, as well as the current move number.

            Returns:
                (String) Game state and move number.
        """
        return str(self.board[(0, 0, 0)]) + "--------" + str(self.board[(0, 1, 0)]) + "--------" + str(
            self.board[(0, 2, 0)]) \
               + "\n|        |        |" \
               + "\n|  " + str(self.board[(1, 0, 0)]) + "-----" + str(self.board[(1, 1, 0)]) + "-----" + str(
            self.board[(1, 2, 0)]) + "  |" \
               + "\n|  |     |     |  |" \
               + "\n|  |  " + str(self.board[(2, 0, 0)]) + "--" + str(self.board[(2, 1, 0)]) + "--" + str(
            self.board[(2, 2, 0)]) + "  |  |" \
               + "\n|  |  |     |  |  |" \
               + "\n" + str(self.board[(0, 0, 1)]) + "--" + str(self.board[(1, 0, 1)]) + "--" + str(
            self.board[(2, 0, 1)]) + "     " + str(self.board[(2, 2, 1)]) + "--" + str(
            self.board[(1, 2, 1)]) + "--" + str(self.board[(0, 2, 1)]) \
               + "\n|  |  |     |  |  |" \
               + "\n|  |  " + str(self.board[(2, 0, 2)]) + "--" + str(self.board[(2, 1, 2)]) + "--" + str(
            self.board[(2, 2, 2)]) + "  |  |" \
               + "\n|  |     |     |  |" \
               + "\n|  " + str(self.board[(1, 0, 2)]) + "-----" + str(self.board[(1, 1, 2)]) + "-----" + str(
            self.board[(1, 2, 2)]) + "  |" \
               + "\n|        |        |" \
               + "\n" + str(self.board[(0, 0, 2)]) + "--------" + str(self.board[(0, 1, 2)]) + "--------" + str(
            self.board[(0, 2, 2)]) \
               + "\n" + "Move nr: " + str(self.number_of_moves_made)

    def pre_hash(self):
        """
            Calculates a number that is a unique representation of every game state with the move number excluded.

            Returns:
                (Integer) return_value: Game state identity.
        """
        return_value = 0  # This will be calculated as a trinary value with every bit representing one position
        for _, value in self.board.items():
            # Assumes the order of iteration will always be the same for a dict() when no entries are added or deleted
            return_value = return_value * 3
            return_value += value
        return_value = return_value * 27  # 3 bits will represent the following information
        if self.number_of_moves_made < 18:
            return_value += self.number_of_moves_made  # 18 first move (placement phase) will be represented as 0 to 17.
        else:
            return_value += self._get_current_player_color() + 17  # blacks turn will be represented as 18 and white 19
        return return_value

    def apply_move(self, move_obj):
        """
            Makes a move in the game state. Requires the usage of the Move class to create a Move object as argument.

            Args:
                (Move) move_obj: Must be a legal move for the game state. Can have three different coordinates, its original position,
                the position it will go to, and the position of the stone it will take.

            Post:
                The state have changed to represent the game after the move have been made.
        """
        move_from, move_to, take_coordinate = move_obj.get_coordinates()
        if move_obj.is_taking():
            self.board[take_coordinate] = BOARD_SLOT.empty

        if not move_obj.is_placement_phase():
            self.board[move_from] = BOARD_SLOT.empty
        self.board[move_to] = self._get_current_player_color()
        self.number_of_moves_made += 1

    def rewind_move(self, move_obj):
        """
            Rewinds a move in the game state. Requires the usage of the Move class to create a Move object as argument.

            Args:
                (Move) move_object Must be a legal move for the game state. Can have three different coordinates, its original position,
                the position it went to, and the position of the stone it took.

            Post:
                The state have changed to represent the game before the move was made.
        """
        move_from, move_to, take_coordinate = move_obj.get_coordinates()
        if move_obj.is_taking():
            self.board[take_coordinate] = self._get_current_player_color()
        if not move_obj.is_placement_phase():
            self.board[move_from] = self._get_opponent_color()
        self.board[move_to] = BOARD_SLOT.empty
        self.number_of_moves_made -= 1

    def get_all_possible_moves(self):
        """
            Gets all the legal moves that the player can do

            Returns:
                (List, Move) Legal/possible move objects.
        """
        phase = self._get_phase()
        if phase == PHASE_PROPERTY.placement_phase:
            return self._create_placement_phase_moves()
        elif phase == PHASE_PROPERTY.movement_phase:
            return self._create_movement_phase_moves()
        elif phase == PHASE_PROPERTY.end_phase:
            return self._create_end_phase_moves()

    def is_draw(self):
        """
            Checks if the game is a draw

            Returns:
                (Boolean) If draw or not.
        """
        return self.number_of_moves_made >= 100

    def is_win(self):
        """
           Checks if someone has won.

           Returns:
           (Boolean) If someone has won or not.
        """

        return self.get_all_possible_moves() == [] or (
                len(self._get_coordinates(self._get_current_player_color())) < 3 and
                self._get_phase() != PHASE_PROPERTY.placement_phase)

    # ----------- PRIVATE METHODS -------------
    def _get_phase(self):
        """
            Gets the current phase of the game state.

            Returns:
            (Integer) The current game phase. 0 for placement phase, 1 for movement phase, 2 for end phase.
        """
        if self.number_of_moves_made < 18:
            return PHASE_PROPERTY.placement_phase
        else:
            no_stones_current_player = 0
            current_color = self._get_current_player_color()
            for _, value in self.board.items():
                if value == current_color:
                    no_stones_current_player += 1

            if no_stones_current_player > 3:
                return PHASE_PROPERTY.movement_phase
            else:
                return PHASE_PROPERTY.end_phase

    def _get_current_player_color(self):
        """
            Gets the color of the stone to be moved. Black if the move number is even and white if the move number is odd.

            Returns:
                (Integer) The color of the stone to be moved. 1 for black, 2 for white.
        """
        if self.number_of_moves_made % 2 == 0:
            return BOARD_SLOT.black
        else:
            return BOARD_SLOT.white

    def _get_opponent_color(self):
        """
            Gets the color of the stone not to be moved. White if the move number is even and black if the move number is odd.

            Returns:
                (Integer) The color of the stone not to be moved. 1 for black, 2 for white.
        """

        if self.number_of_moves_made % 2 == 1:
            return BOARD_SLOT.black
        else:
            return BOARD_SLOT.white

    def _create_placement_phase_moves(self):
        """
            Creates moves for the placement phase

            Returns:
                (List, Move) list_of_moves: Legal/possible move objects during the placement phase.
        """
        empty_coordinates = self._get_coordinates(BOARD_SLOT.empty)
        list_of_moves = []
        for coord in empty_coordinates:
            if self._move_gives_three_in_row(None, coord, self._get_current_player_color()):
                self._get_taking_moves(list_of_moves, MOVE_PROPERTY.placement_phase, coord)
            else:
                move_obj = Move(MOVE_PROPERTY.placement_phase, coord, MOVE_PROPERTY.not_taking)
                list_of_moves.append(move_obj)
        return list_of_moves

    def _create_end_phase_moves(self):
        """
            Creates moves for the end phase

            Returns:
                (List, Move) list_of_moves: Legal/possible move objects during the end phase.
         """
        empty_coordinates = self._get_coordinates(BOARD_SLOT.empty)
        current_player_coordinates = self._get_coordinates(self._get_current_player_color())
        list_of_moves = []
        for move_from in current_player_coordinates:
            for coord in empty_coordinates:
                if self._move_gives_three_in_row(move_from, coord, self._get_current_player_color()):
                    self._get_taking_moves(list_of_moves, move_from, coord)
                else:
                    move_obj = Move(move_from, coord, MOVE_PROPERTY.not_taking)
                    list_of_moves.append(move_obj)

        return list_of_moves

    def _create_movement_phase_moves(self):
        """
            Creates moves for the movement phase

            Returns:
                (List, Move) list_of_moves: Legal/possible move objects during the movement phase.
        """
        current_player_color = self._get_current_player_color()
        current_player_coordinates = self._get_coordinates(current_player_color)
        list_of_moves = []

        for move_from in current_player_coordinates:  # Will try to move every friendly stone
            for i in range(6):  # 3 dim and 2 possible moves in each dim
                move_from_list = list(move_from)  # can't manipulate tuples
                if move_from_list[1] == 1 or move_from_list[2] == 1 or i // 2 != 0:  # removes corner moves in x dim
                    move_from_list[i // 2] += (i % 2) * 2 - 1  # this will alternate between -1 and 1
                    move_to = tuple(move_from_list)  # A destination to do some checks on

                    if self._check_coordinate(move_to, BOARD_SLOT.empty):
                        # removes moves outside board and to nonempty BOARD_SLOTS
                        if self._move_gives_three_in_row(move_from, move_to, current_player_color):  # if takes
                            self._get_taking_moves(list_of_moves, move_from, move_to)

                        else:  # if not takes
                            move_obj = Move(move_from, move_to, MOVE_PROPERTY.not_taking)
                            list_of_moves.append(move_obj)
        return list_of_moves

    def _get_taking_moves(self, list_of_moves, move_from, move_to):
        """
        Gets all possible stones that can be taken if move_to results in a three in a row

            Args:
                (List, Move) list_of_moves: moves to be appended
                (3x3x3 tuple) move_from: origin of the move to be appended
                (3x3x3 tuple) move_to: destination of the move to be appended

            Post:
                All possible moves to take an enemy stone is added to list_of_moves
        """
        opponent_coordinates = self._get_coordinates(self._get_opponent_color())
        all_part_of_mills = True
        for key, _ in opponent_coordinates.items():  # can pick any enemy stone ...
            if not self._move_gives_three_in_row(None, key, self._get_opponent_color()):
                # ... if it doesn't give 3 in row
                move_obj = Move(move_from, move_to, key)
                if len(opponent_coordinates) <= 3 and self.number_of_moves_made >= 18:  # Condition for winning
                    move_obj.set_winning()
                list_of_moves.append(move_obj)
                all_part_of_mills = False
        if all_part_of_mills:
            # If all enemy stones are in mills you can take anyone. Will almost never be the case.
            for key, _ in opponent_coordinates.items():  # can pick any enemy stone.
                move_obj = Move(move_from, move_to, key)
                if len(opponent_coordinates) <= 3 and self.number_of_moves_made >= 18:  # Condition for winning
                    move_obj.set_winning()
                list_of_moves.append(move_obj)

    def _move_gives_three_in_row(self, move_from, move_to, color_to_move):
        """
            Checks if a move gives three in a row

            Args:
                (3x3x3 tuple) move_from: Original coordinate of the stone
                (3x3x3 tuple) move_to: New coordinate of the stone
                (Integer) color_to_move: The color of the stone to be moved. 1 for black, 2 for white.

            Returns:
                (Boolean) True if the move gives three in a row. False if not.
        """
        for i in range(3):  # 3 dim to get 3 in raw in
            if move_to[1] == 1 or move_to[2] == 1 or i != 0:
                # prevents to moving up in corners and prevents
                coord = list(move_to)
                coord[i] = (coord[i] + 1) % 3
                tuple1 = tuple(coord)
                coord[i] = (coord[i] + 1) % 3
                tuple2 = tuple(coord)
                if tuple1 != move_from and tuple2 != move_from and \
                        self._check_coordinate(tuple1, color_to_move) and \
                        self._check_coordinate(tuple2, color_to_move):
                    # First se if coord1 and coord2 is not the stone being moved.
                    return True
        return False

    def _check_coordinate(self, coordinate, value):
        """
            Checks if a position on the board has a certain stone or not.

            Args:
                (3x3x3 tuple) coordinate: Coordinate of the position to be checked.
                (Integer) value: Value of the position. 0 for no stone, 1 for black stone, 2 for white stone.

            Returns:
                (Boolean) True if the coordinate exists and has the specified value
        """
        return coordinate in self.board and self.board[coordinate] == value

    def _get_coordinates(self, color):
        """
            Gets all the positions where the value is equal to the one specified in the argument.

            Args:
                (Integer) color: Value of the desired positions. 0 for no stone, 1 for black stone, 2 for white stone.

            Returns:
                (Dict, 3x3x3 tuples: Integer) Coordinates with the specified value.
        """
        coordinates_for_color = {}
        for key, value in self.board.items():
            if value == color:
                coordinates_for_color[key] = value
        return coordinates_for_color

    def _check_nr_stones(self, color_nr):
        """
                Gets the number of stones of the color specified in the argument.

                Args:
                    (Integer) color: Value of the desired color. 1 for black stone, 2 for white stone.

                Returns:
                    (Integer) Number of stones.
        """
        stones = 0
        for _, value in self.board.items():
            if value == color_nr:
                stones += 1
        return stones
