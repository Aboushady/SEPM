from .utils import *


class Move:
    """
        Move class. This class has methods and attributes for representing how Move's are defined.
        Has attributes: move_from, move_to and take_coordinate
    """

    def __init__(self, move_from, move_to, take_coordinate):
        """
            Constructor of the Move class. Will have three different values to specify its properties.

            Args:
                (3x3x3 tuple) moves_from: Original coordinate of the stone. (-1, -1, -1) if a stone is placed and not moved.
                (3x3x3 tuple) moves_to: New coordinate of the stone.
                (3x3x3 tuple) take_coordinate: Coordinate of stone to be taken. (-1,-1,-1) if no stone is taken.
        """
        self.move_from = move_from
        self.move_to = move_to
        self.take_coordinate = take_coordinate
        self.__winning = False
        self.__drawing = False

    def is_taking(self):
        """
            Tells if the Move object is taking a stone.

            Returns:
                (Boolean) True if take_coordinate does not have the same coordinates as MOVE_PROPERTY.not_taking, which is (-1,-1,-1).
        """

        return not self.take_coordinate == MOVE_PROPERTY.not_taking

    def is_placement_phase(self):
        """
            Tells if the Move object is placed during the placement phase.

            Returns:
                (Boolean) True if move_from has the same coordinates as MOVE_PROPERTY.placement_phase, which is (-1,-1,-1).
        """
        return self.move_from == MOVE_PROPERTY.placement_phase

    def is_winning(self):
        """
            Tells if the Move object is going to make its player win the game.

            Returns:
                (Boolean) self.__winning
        """
        return self.__winning

    def set_winning(self):
        """
            Makes it so that the Move object has the property of winning the game.

            Post:
                self.__winning is set to true
        """
        self.__winning = True

    def is_drawing(self):
        """
            Tells if the Move object is going to make its player draw the game.

            Returns:
                (Boolean) self.__drawing
        """
        return self.__drawing

    def set_drawing(self):
        """
            Makes it so that the Move object has the property of drawing the game

            Post:
                self.__drawing is set to true
        """
        self.__drawing = True

    def get_coordinates(self):
        """
            Gets the properties of the Move object.

            Returns:
                (3x3x3 tuple) moves_from: Original coordinate of the stone. (-1, -1, -1) if a stone is placed and not moved.
                (3x3x3 tuple) moves_to: New coordinate of the stone.
                (3x3x3 tuple) take_coordinate: Coordinate of stone to be taken. (-1,-1,-1) if no stone is taken.
        """
        return self.move_from, self.move_to, self.take_coordinate

    def __str__(self):
        """
            Prints the properties of the Move object.

            Returns:
                (String) move_from, move_to, take_coordinate.
        """
        return f'({self.move_from[0]}, {self.move_from[1]}, {self.move_from[2]}),\
            ({self.move_to[0]}, {self.move_to[1]}, {self.move_to[2]}),\
            ({self.take_coordinate[0]}, {self.take_coordinate[1]}, {self.take_coordinate[2]})'
