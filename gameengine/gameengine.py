from .gamestate import GameState
from .ai import AI
from .utils import *


class GameEngine:
    """
        GameEngine class. This is the class with external methods that the other components may use.
    """

    def __init__(self, ai_level=2, game_state=GameState()):
        """
            Constructor of the game engine: Creates an AI object since it needs save a hash table between moves
            in order to not search the same state more then once. This makes the searching faster.

            Also makes an initial game state that ai and human moves will be applied to.

            Args:
                (Integer) ai_level: The difficulty level of the AI: 1 (easy), 2 (medium), 3 (hard)
                (GameState) game_state: (Optional) If you want the AI to play on a specific GameState.
        """
        self.ai = AI(ai_level)
        self.game_state = game_state

    def ai_move(self):
        """
            The AI will make a move and then apply the move to the internal game state.
            It will return 3 coordinates representing the move.

            (Special case): If no legal moves are possible, all return values will be None

            Returns:
                (3x3x3 tuple) move_from: Coordinates of the stone to move (None if placement phase)
                (3x3x3 tuple) move_to: Coordinates of the destination
                (3x3x3 tuple) move_take: Coordinates of the stone to take (None if no stone is taken)
        """
        if not self.game_state.get_all_possible_moves():
            return None, None, None

        best_move = self.ai.get_best_move(self.game_state)
        move_from, move_to, move_take = best_move.get_coordinates()

        if not best_move.is_taking():
            move_take = None

        if best_move.is_placement_phase():
            move_from = None

        return move_from, move_to, move_take

    def human_move(self, move_from, move_to, move_take=None):
        """
            Applies the human move to the internal game state.

            Args:
                (3x3x3 tuple) move_from: Coordinates of the stone to move (None if placement phase)
                (3x3x3 tuple) move_to: Coordinates of the destination
                (3x3x3 tuple) move_take: Coordinates of the stone to take (None if no stone is taken)

            Returns:
                (Boolean) True, if the move is valid. False, if not.
        """
        if not move_from or self.game_state._get_phase() == PHASE_PROPERTY.placement_phase:
            move_from = MOVE_PROPERTY.placement_phase
        if not move_take:
            move_take = MOVE_PROPERTY.not_taking

        for legal_move in self.game_state.get_all_possible_moves():
            legal_from, legal_to, legal_take = legal_move.get_coordinates()

            if legal_from == move_from and legal_to == move_to and legal_take == move_take:
                self.game_state.apply_move(legal_move)
                return True
        return False

    @staticmethod
    def convert_from_seven_x_seven(seven_x_seven_list):
        """
            Converts a list of 7 x 7 coordinates tuples (x , y)
            to a list of 3 x 3 x 3 coordinate tuples (square, x, y)

            Args:
                (List, 7x7 tuple) seven_x_seven_list: 7x7 board positions as tuples (x, y),
                upper left corner being (0, 0)

            Returns:
                (List, 3x3x3 tuple) return_list: 3x3x3 board positions (square, x, y),
                upper left corner being (0, 0, 0). See D2 for in depth explanation.
        """
        return_list = []
        for seven_x_seven in seven_x_seven_list:
            if seven_x_seven:
                if seven_x_seven[0] == 2 or seven_x_seven[0] == 4 or seven_x_seven[1] == 2 or seven_x_seven[1] == 4:
                    # 2:nd square
                    return_list.append((2, seven_x_seven[0]-2, seven_x_seven[1]-2))
                elif seven_x_seven[0] == 1 or seven_x_seven[0] == 5 or seven_x_seven[1] == 1 or seven_x_seven[1] == 5:
                    # 1:st square
                    return_list.append((1, (seven_x_seven[0] - 1)//2, (seven_x_seven[1] - 1)//2))
                elif seven_x_seven[0] == 0 or seven_x_seven[0] == 6 or seven_x_seven[1] == 0 or seven_x_seven[1] == 6:
                    # 0:st square
                    return_list.append((0, seven_x_seven[0]//3, seven_x_seven[1]//3))
        return return_list

    @staticmethod
    def convert_to_seven_x_seven(three_x_three_x_three_list):
        """
            Converts a list of 3 x 3 x 3 coordinate tuples (square, x, y)
            to a list of 7 x 7 coordinate tuples (x , y)

            Args:
                (List, 3x3x3 tuple)three_x_three_x_three_list: 3x3x3 board positions (square, x, y),
                 upper left corner being (0, 0, 0). See D2 for in depth explanation.
            Returns:
                (List, 7x7 tuple) return_list: 7x7 board positions as tuple (x, y),
                 upper left corner being (0, 0)
        """
        return_list = []
        for three_x_three_x_three in three_x_three_x_three_list:
            if three_x_three_x_three:
                if three_x_three_x_three[0] == 2:
                    # 2:nd square
                    return_list.append((2 + three_x_three_x_three[1], 2 + three_x_three_x_three[2]))
                if three_x_three_x_three[0] == 1:
                    # 1:st square
                    return_list.append((1 + three_x_three_x_three[1] * 2, 1 + three_x_three_x_three[2] * 2))
                if three_x_three_x_three[0] == 0:
                    # 0:st square
                    return_list.append((three_x_three_x_three[1] * 3, three_x_three_x_three[2] * 3))
        return return_list

    def is_win(self):
        return self.game_state.is_win()

    def is_draw(self):
        return self.game_state.is_draw()

    def __str__(self):
        return str(self.game_state)
