from collections import OrderedDict
from .utils import *
from .gamestate import GameState
STONE_VALUE = 1
ALPHA = 1.72  # Moves with this value will be considered good enough
DISCOUNT_FACTOR = 0.95  # Values will decrease for every step deeper in the tree they occur
WINNING_VALUE = 100
MAX_DEPTH = 7
MEDIUM_DEPTH = 4
EASY_DEPTH = 2
MAX_HASH_ENTRIES = 1024*1024*1024/256  # Max 1gb if every entry takes less then 256 bytes


class AI:
    """
        AI Class. This class contains the settings and methods that the AI uses for determining the best move according
        to a difficulty.
    """
    def __init__(self, ai_level=3):
        """
            Constructor of the ai: Creates an Ordered Dict object to use as a hash table
            in order to not search the same state more then once. This makes the searching (much) faster.

            Args:
                (Integer) ai_level: The difficulty level of the AI: 1 (easy), 2 (medium), 3 (hard)
        """

        self.hash_map = OrderedDict()
        self.ai_level = ai_level

    def get_best_move(self, board):
        """
            Gets the best move in a state of the game up to a maximal depth depending on ai_level.

            Post: The best legal move is applied to the board

            Args:
                (GameState) board: Object of type GameState for which to find the best move.

            Returns:
                (Move) best_move: Move object representing the best legal move
        """
        if board.get_number_of_moves_made() < 7:
            max_depth = 5
        elif board.get_number_of_moves_made() < 15:
            max_depth = 6
        else:
            max_depth = 7

        if self.ai_level == 3:
            depth = min(max_depth, MAX_DEPTH)
        elif self.ai_level == 2:
            depth = min(max_depth, MEDIUM_DEPTH)
        else:
            depth = min(max_depth, EASY_DEPTH)

        if board._get_current_player_color() == BOARD_SLOT.black:
            sign = 1
        else:
            sign = -1

        (_, best_move) = self.__tree_search(board, depth, sign)
        board.apply_move(best_move)
        if board.is_win():
            best_move.set_winning()
        elif board.is_draw():
            best_move.set_drawing()

        return best_move

    def __tree_search(self, board, depth, sign):
        """
            Recursively finds the value of the best move in a state. sign variable decides if the value should be
            counted negatively or positively.

            To evaluate the next state, a recursive call to tree_search with opposite sign is called since good moves
            from the opponent need to have the opposite effect on the value.

            Args:
                (GameState) board: Object of type game state that represent the board
                (Integer) depth: How many recursive steps that will be considered when valuing a state.
                sign: +1 or -1, To count values positively or negatively

            Returns:
                (best_value, best_move). best_move is the move with the best value.
        """
        if depth <= 0:
            return 0, None
        pre_hash = board.pre_hash()
        if pre_hash in self.hash_map:
            (value_from_hash, depth_from_hash, move_from_hash) = self.hash_map[pre_hash]
            if depth_from_hash >= depth:
                return value_from_hash * DISCOUNT_FACTOR, move_from_hash
            else:
                self.hash_map.pop(pre_hash)  # removes the old entry, else the age of the entry will not be refreshed

        if len(self.hash_map) >= MAX_HASH_ENTRIES/2:
            self.hash_map.popitem(False)  # throwing out the oldest element if hash_map is too large
            print("hash removed")

        best_value = 0
        best_move = None

        for move in board.get_all_possible_moves():
            if move.is_winning():
                self.hash_map[pre_hash] = (WINNING_VALUE * sign, MAX_DEPTH, move)
                return (WINNING_VALUE * sign), move
            board.apply_move(move)
            tmp_value, _ = self.__tree_search(board, depth-1, sign*(-1))
            board.rewind_move(move)

            if move.is_taking():
                tmp_value += STONE_VALUE * sign
            if (not best_move) or tmp_value * sign > best_value * sign:
                best_value = tmp_value
                best_move = move
                if tmp_value * sign >= ALPHA:
                    # alpha-beta pruning, stops searching after it found a very good move
                    break

        if not best_move:
            self.hash_map[pre_hash] = (- WINNING_VALUE * sign, MAX_DEPTH, None)
            return (- WINNING_VALUE * sign), best_move

        if best_value <= - WINNING_VALUE + MAX_DEPTH * STONE_VALUE \
                or best_value >= WINNING_VALUE - MAX_DEPTH * STONE_VALUE:
            depth = MAX_DEPTH

        self.hash_map[pre_hash] = (best_value, depth, best_move)
        return (best_value * DISCOUNT_FACTOR), best_move
