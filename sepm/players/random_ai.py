"""Random AI module."""

import random
import time

from sepm import Phase
from sepm import PieceColor as Color
from sepm.exceptions import FoundMillError
from sepm.players import Player


class RandomAI(Player):
    """AI which places stones randomly."""

    def __init__(self, name, color, delay=0.5, num_pieces=9, phase=Phase.placing):
        super().__init__(name, color, num_pieces, phase)
        self.delay_time = delay

    def delay(self):
        """Let the AI sleep before continuing."""
        time.sleep(self.delay_time)

    def handle_place(self, board):
        """Handle placing a stone on the board (in phase 'placing')."""
        piece = self.pieces.pop()

        def place():
            node = random.choice(board.empty_nodes())
            return board.place(node.key, piece)

        self.do_move(
            place, error_msg='AI failed to place stone, trying again...')
        self.delay()

    def handle_move(self, board):
        """Handle moving a stone on the board (in phase 'moving')."""
        def move():
            try:
                from_node = random.choice(board.nodes(color=self.color))
                to_node = random.choice(
                    list(from_node.empty_neighbors.values()))
                return board.move(from_node.key, to_node.key)
            except IndexError:
                return False

        # self.do_move(move, error_msg='AI failed to move stone, trying again...')
        self.do_move(move, error_msg=None)
        self.delay()

    def handle_fly(self, board):
        """Handle flying a stone on the board (in phase 'flying')."""
        def fly():
            try:
                from_node = random.choice(board.nodes(color=self.color))
                to_node = random.choice(board.empty_nodes())
                return board.fly(from_node.key, to_node.key)
            except IndexError:
                return False

        self.do_move(fly, error_msg='AI failed to move stone, trying again...')
        self.delay()

    def handle_mill(self, board):
        """Handle when a mill was formed."""
        def mill():
            removed_position = random.choice(board.nodes(self.opponent_color))
            return board.remove(removed_position.key)

        self.do_move(
            mill, error_msg='AI failed to remove stone, trying again...')
        self.delay()
