"""Human player module."""

from sepm import check_valid_pos
from sepm.exceptions import GameOver
from sepm.players import Player


class HumanPlayer(Player):
    """Human controlled player class."""

    def _select_node(self, board, msg):
        """Request user input and try to get the node corresponding to position supplied"""
        while True:
            pos = input('{}\n> '.format(msg)).lower()
            if pos == 'q' or pos == 'quit':
                raise GameOver(winner=None)
            elif pos == 'r' or pos == 'resign':
                raise GameOver(winner=board.players[self.opponent_color])
            try:
                pos = check_valid_pos(pos)
                if not pos:
                    raise KeyError()
                return board.get_node(pos)
            except KeyError:
                print("Invalid position, try again!")

    def handle_place(self, board):
        """Handle placing a stone on the board (in phase 'placing')."""
        piece = self.pieces.pop()

        def place():
            node = self._select_node(board, 'Enter position to place stone:')
            return board.place(node.key, piece)
        self.do_move(place, error_msg='Unable to place stone at that position')

    def handle_move(self, board):
        """Handle moving a stone on the board (in phase 'moving')."""
        def move():
            from_node = self._select_node(board, 'Enter position to move stone from:')
            while from_node.piece is None:
                redo_msg = 'Only positions where ' + self.color.value + ' pieces exist are acceptable, try again: '
                from_node = self._select_node(board, redo_msg)
            to_node = self._select_node(board, 'Enter position to move the stone to:')
            return board.move(from_node.key, to_node.key)
        self.do_move(move, error_msg='Unable to move stone to that position')

    def handle_fly(self, board):
        """Handle flying a stone on the board (in phase 'flying')."""
        def fly():
            from_node = self._select_node(board, 'Enter position to move stone from:')
            while from_node.piece is None:
                redo_msg = 'Only positions where ' + self.color.value + ' pieces exist are acceptable, try again: '
                from_node = self._select_node(board, redo_msg)
            to_node = self._select_node(
                board, 'Enter position to move the stone to:')
            return board.fly(from_node.key, to_node.key)
        self.do_move(fly, error_msg='Unable to move stone to that position')

    def handle_mill(self, board):
        """Handle when a mill was formed."""
        print('You formed a mill! ', end='')

        def mill():
            node = self._select_node(board, 'Enter stone to remove:')
            return board.remove(node.key)
        self.do_move(mill, error_msg='Unable to remove that stone')
