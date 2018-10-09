"""Player module."""

from enum import Enum

from sepm import GamePiece, Phase, PieceColor as Color


class Player:
    """Class that represents a player."""

    def __init__(self, name, color, num_pieces=9, phase=Phase.placing):
        """Initialize a new player."""
        self.name = name
        self.color = color
        self.phase = phase
        self.pieces = [GamePiece(color) for _ in range(num_pieces)]
        self.last_move = [None, None]

    @property
    def opponent_color(self):
        """Get the opponent's color."""
        if self.color is None:
            return None
        return Color.White if self.color == Color.Black else Color.Black

    @property
    def is_placing(self):
        """Is the player in the placing phase?"""
        return self.phase == Phase.placing

    @property
    def is_moving(self):
        """Is the player in the moving phase?"""
        return self.phase == Phase.moving

    @property
    def is_flying(self):
        """Is the player in the flying phase?"""
        return self.phase == Phase.flying

    def do_move(self, move_fun, error_msg):
        """Perform a move until it's successful."""
        while not move_fun():
            if error_msg is not None:
                print(error_msg)

    def handle_place(self, board):
        """
        Handle placing a stone on the board (in phase 'placing').

        Abstract method, should be implemented in the Player sub-classes.

        :param board: GameBoard object to make a move on
        """
        raise NotImplementedError('Abstract handle_place() method')

    def handle_move(self, board):
        """
        Handle moving a stone on the board (in phase 'moving').

        Abstract method, should be implemented in the Player sub-classes.

        :param board: GameBoard object to make a move on
        """
        raise NotImplementedError('Abstract handle_move() method')

    def handle_fly(self, board):
        """
        Handle flying a stone on the board (in phase 'flying').

        Abstract method, should be implemented in the Player sub-classes.

        :param board: GameBoard object to make a move on
        """
        raise NotImplementedError('Abstract handle_fly() method')

    def handle_mill(self, board):
        """
        Handle when a mill was formed.

        Abstract method, should be implemented in the Player sub-classes.

        :param board: GameBoard object to make a move on
        """
        raise NotImplementedError('Abstract handle_mill() method')

    def __str__(self):
        return self.name
