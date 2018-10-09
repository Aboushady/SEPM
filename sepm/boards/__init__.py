"""Game board module."""

import re
import time

from enum import Enum

from sepm import PieceColor as Color, GamePiece, Phase
from sepm.exceptions import FoundMillError, GameOver


RE_NODE = re.compile(r'(?P<key>\w+)\s*=\s*(?P<value>\w+),?')


class Node:
    def __init__(self, key, piece=None, neighbors={}):
        self._key = key
        self._piece = piece
        self._neighbors = dict(neighbors)

    @property
    def is_empty(self):
        """A node is empty if its piece is None."""
        return self._piece is None

    @property
    def key(self):
        return self._key

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, piece):
        self._piece = piece

    @property
    def neighbors(self):
        return self._neighbors

    @property
    def empty_neighbors(self):
        return {pos: node for pos, node in self._neighbors.items() if node.is_empty}

    def add_neighbors(self, **neighbors):
        for direction, node in neighbors.items():
            self._neighbors[direction] = node

    def has_neighbor(self, position):
        """Check if a node has a neighbor in the given position."""
        for node in self._neighbors.values():
            if node.key == position:
                return True
        return False

    def next(self, direction):
        return self._neighbors[direction]

    def __repr__(self):
        """String representation of a Node."""
        neighbors = [
            '%s=%s' % (dir, node.key)
            for dir, node in self._neighbors.items()
        ]
        return 'Node(key={}, piece={}, neighbors={{{}}})'.format(
            self.key, self.piece, ', '.join(neighbors)
        )


class GameBoard(object):
    """Representation of the game board."""

    def __init__(self, max_time=1800, max_moves=50):
        """Initiate a new game board."""
        self.state = self._build_graph()
        self.current = None
        self._black_moves = 0
        self._white_moves = 0
        self._max_moves = max_moves
        self._max_time = max_time
        self._time = time.time()
        self.players = {
            Color.White: None,
            Color.Black: None
        }

    def _build_graph(self):
        """Build and returns graph with the nodes for the game board (abstract)."""
        raise NotImplementedError()

    def _load_graph_from_file(self, filename):
        """Load graph from file."""
        nodes = {}

        def create_or_find_node(position, dir=None, parent=None):
            """Create node or find node by position then add opposing direction as neighbor."""
            if position not in nodes:
                nodes[position] = Node(position)
            node = nodes[position]
            if dir is not None and parent is not None:
                if dir == 'up':
                    node.add_neighbors(down=parent)
                elif dir == 'down':
                    node.add_neighbors(up=parent)
                elif dir == 'left':
                    node.add_neighbors(right=parent)
                elif dir == 'right':
                    node.add_neighbors(left=parent)
            return node

        def parse_node_line(line):
            """Parse a Node from a line in the nodes file format."""
            position, raw_neighbors = [x.strip() for x in line.split(':')]
            nodes[position] = create_or_find_node(position)
            neighbors = {}
            for m in RE_NODE.finditer(raw_neighbors):
                dir, neighbor_node = m.groups()
                neighbors[dir] = create_or_find_node(
                    neighbor_node, dir=dir, parent=nodes[position])
            nodes[position].add_neighbors(**neighbors)

        with open(filename, 'r') as f:
            # Validate .nodes file format
            if not next(f).startswith('#!nmm_nodes'):
                raise TypeError('Invalid .nodes file format')

            # Parse nodes
            for line in f:
                if line.startswith('#'):
                    continue  # skip comments
                parse_node_line(line.strip())
        return nodes

    @property
    def max_moves(self):
        return self._max_moves

    @property
    def max_time(self):
        return self._max_time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self):
        self._time = time.time()

    @property
    def black_moves(self):
        return self._black_moves

    def incerement_black_moves(self, number=1):
        self._black_moves += number

    @property
    def white_moves(self):
        return self._white_moves

    def incerement_white_moves(self, number=1):
        self._white_moves += number

    @property
    def has_white_player(self):
        """Check if the game has a white player."""
        return self.players[Color.White] is not None

    @property
    def has_black_player(self):
        """Check if the game has a black player."""
        return self.players[Color.Black] is not None

    @property
    def white_count(self):
        """Get the number of white pieces on the board."""
        return self.count_pieces(Color.White)

    @property
    def black_count(self):
        """Get the number of white pieces on the board."""
        return self.count_pieces(Color.Black)

    def count_pieces(self, color):
        """Get the number of pieces on the board with the given color."""
        nodes = self.state.values()
        return sum(1 for n in nodes if not n.is_empty and n.piece.color == color)

    def add_player(self, color, player):
        """Add a new player to the game."""
        self.players[color] = player

    def change_turn(self):
        """Change player turn."""
        self.update_phase()
        self.game_over()

        if self.current is None:
            self.current = self.players[Color.Black]
        else:
            if self.current.color == Color.White:
                self.current = self.players[Color.Black]
                self.incerement_black_moves()
            else:
                self.current = self.players[Color.White]
                self.incerement_white_moves()

    def count_nodes_direction(self, position, direction):
        """Get the node count with the same color in one direction."""
        try:
            color = self.get_piece(position).color
            nodes = self.iter_nodes(position, direction)
            return sum(1 for n in nodes if not n.is_empty and n.piece.color == color)
        except AttributeError:
            return 0

    def check_mill(self, position):
        """
        Check if a mill has occurred.

        :return: True if a mill was found, otherwise False.
        """
        raise NotImplementedError()  # AbstractMethodException

    def empty_nodes(self, moving_color=None):
        """
        Get a list of empty nodes.

        If moving_color is specified, only nodes adjacent to the nodes that belong
        to that color are returned.
        """
        if moving_color is not None:
            # Return all empty nodes around the given node
            nodes = self.nodes(color=moving_color)
            empty_nodes = []
            for node in nodes:
                for n in node.neighbors.values():
                    if n.is_empty:
                        empty_nodes.append(n)
            return empty_nodes
        else:
            # Return all empty nodes
            return [n for n in self.state.values() if n.is_empty]

    def nodes(self, color=None):
        """Get all nodes with a piece that has the given color."""
        if color is None:
            return self.state.values()

        return [n for n in self.state.values() if not n.is_empty and n.piece.color == color]

    def mill_lock(self, color):
        """Checks if pieces are in a mill lock."""
        my_nodes = self.nodes(color)
        result = True
        for node in my_nodes:
            result = result and self.check_mill(node.key)
        return result

    def update_phase(self):
        """Update player's phase."""
        for player in self.players.values():
            piece_count = len(player.pieces)
            if piece_count > 0:
                if not player.is_placing:
                    player.phase = Phase.placing
            else:
                board_piece_count = self.count_pieces(player.color)
                if board_piece_count > 3 and not player.is_moving:
                    player.phase = Phase.moving
                elif board_piece_count == 3 and not player.is_flying:
                    player.phase = Phase.flying

    def get_node(self, position):
        """Get node on board on position.

        :raises KeyError: On invalid board position
        :return: GamePiece object
        """
        try:
            return self.state[position]
        except KeyError:
            raise KeyError('Invalid game board position: {}'.format(position))

    def get_piece(self, position):
        """Get piece on board on position.

        :raises KeyError: On invalid board position
        :return: GamePiece object
        """
        return self.get_node(position).piece

    def occupied_node(self, position):
        """Check if there is a piece on board on position.

        :raises KeyError: On occupied "to_pos" position
        :return: True or False
        """
        try:
            return self.get_node(position).piece is not None
        except KeyError:
            raise KeyError('cant move to occupied node: {}'.format(position))

    def move_lock(self, color):
        """ Checks whether it's possible for any piece to be moved to adjacent position """
        empty_adj_nodes = self.empty_nodes(color)
        return len(empty_adj_nodes) == 0

    def _move_piece(self, from_pos, to_pos):
        """Move a piece from one node to another."""
        piece = self.get_piece(from_pos)
        self.remove(from_pos, True)
        self.place(to_pos, piece)

        if self.check_mill(to_pos):
            raise FoundMillError()

        return True

    def place(self, position, piece):
        """
        Place a piece on the board.

        :raises KeyError: On invalid board position
        :return: True if placement happend, false if position was occupied
        """
        node = self.get_node(position)
        if not node.is_empty:
            return False
        if self.current.color != piece.color:
            return False

        node.piece = piece
        if self.check_mill(position):
            raise FoundMillError()

        return True

    def move(self, from_pos, to_pos):
        """
        Move piece from one node to another.

        :return: True if move was successful
        """
        from_node = self.get_node(from_pos)
        to_node = self.get_node(to_pos)
        valid_player = not from_node.is_empty and from_node.piece.color == self.current.color
        valid_to_node = to_node.is_empty and from_node.has_neighbor(to_pos)
        if valid_to_node and self.current.is_moving and valid_player:
            return self._move_piece(from_pos, to_pos)
        else:
            return False

    def fly(self, from_pos, to_pos):
        """
        Fly piece from one node to another.

        :return: True if move was successful
        """
        from_node = self.get_node(from_pos)
        to_node = self.get_node(to_pos)
        valid_player = not from_node.is_empty and from_node.piece.color == self.current.color and self.current.is_flying
        if to_node.is_empty and valid_player:
            return self._move_piece(from_pos, to_pos)
        else:
            return False

    def remove(self, position, priority=False):
        """Remove piece from one node."""
        if priority:
            self.get_node(position).piece = None
            return True
        piece = self.get_node(position).piece
        if self.occupied_node(position):
            if self.current.color == piece.color:
                return False
            if self.mill_lock(piece.color):
                self.get_node(position).piece = None
                return True
            if not self.check_mill(position):
                self.get_node(position).piece = None
                return True
        return False

    def game_over(self, limit=3):
        white_player = self.players[Color.White]
        black_player = self.players[Color.Black]

        white_moves = self.white_moves
        black_moves = self.black_moves

        if not white_player.is_placing and self.white_count < limit:
            raise GameOver(winner=black_player)

        if not black_player.is_placing and self.black_count < limit:
            raise GameOver(winner=white_player)

        if self.white_count + self.black_count >= len(self.state):
            raise GameOver(winner=None)

        if white_moves + black_moves >= self.max_moves * 2:
            raise GameOver(winner=None)

        if time.time() - self.time > self.max_time:
            raise GameOver(winner=None)

        if self.current is not None:
            if self.current.color == Color.Black and self.move_lock(Color.White) and white_player.is_moving:
                raise GameOver(winner=black_player)
            if self.current.color == Color.White and self.move_lock(Color.Black) and black_player.is_moving:
                raise GameOver(winner=white_player)

    def iter_nodes(self, position, direction):
        """Iterate from the start node to the last node in the given direction."""
        node = self.get_node(position)
        yield node
        while direction in node.neighbors:
            node = node.next(direction)
            yield node
