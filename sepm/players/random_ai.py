"""Random AI module."""

import random
import time

from sepm import Phase
from sepm import PieceColor as Color
from sepm.exceptions import FoundMillError
from sepm.players import Player
from gameengine import gameengine
from gameengine import gamestate
class RandomAI(Player):
    """AI which places stones randomly."""

    def __init__(self, name, color, delay=0.5, num_pieces=9, phase=Phase.placing):
        super().__init__(name, color, num_pieces, phase)
        self.delay_time = delay
        self.mill = None
        
    def delay(self):
        """Let the AI sleep before continuing."""
        time.sleep(self.delay_time)
    def __new_state(self, board):
        #print(board.nodes(self.color))
        print("AI is thinking...\n")
        ge = gameengine.GameEngine(1)
        black = []
        white = []
        blackl = board.nodes(Color.Black)
        whitel = board.nodes(Color.White)
        for i in range(0, len(blackl)):
            black.append(ge.convert_from_seven_x_seven([(ord(blackl[i].key[0])-97, abs(int(blackl[i].key[1])-7))])[0])
            #print(ge.convert_from_seven_x_seven([(ord(blackl[i].key[0])-97, int(blackl[i].key[1])-1)]))
        for i in range(0, len(whitel)):
            white.append(ge.convert_from_seven_x_seven([(ord(whitel[i].key[0])-97, abs(int(whitel[i].key[1])-7))])[0])
            #print(ge.convert_from_seven_x_seven([(ord(whitel[i].key[0])-97, int(whitel[i].key[1])-1)]))
        gs = gamestate.GameState(black, white, board.black_moves+board.white_moves)

        #print(gs)
        return(gameengine.GameEngine(1, gs))#print(gs)
        
    def handle_place(self, board):
        """Handle placing a stone on the board (in phase 'placing')."""
        piece = self.pieces.pop()

        def place():
            #node = random.choice(board.empty_nodes())
            ge = self.__new_state(board)
            move = ge.ai_move()
            move = ge.convert_to_seven_x_seven(list(move))
            #print("mf"+str(move_from))
            #print("mt"+str(chr(move[0][0]+97) + str(abs(move[0][1]-7))))
            if(len(move) == 2):
                self.mill = str(chr(move[1][0]+97) + str(abs(move[1][1]-7)))
            #print("mta"+str(move_take))
            nkey = str(chr(move[0][0]+97) + str(abs(move[0][1]-7)))
            return board.place(nkey, piece)

        self.do_move(
            place, error_msg='AI failed to place stone, trying again...')
        self.delay()

    def handle_move(self, board):
        """Handle moving a stone on the board (in phase 'moving')."""
        def move():
            try:
                ge = self.__new_state(board)
                move = ge.ai_move()
                move = ge.convert_to_seven_x_seven(list(move))
                #print("mf"+str(chr(move[0][0]+97) + str(abs(move[0][1]-7))))
                #print("mt"+str(chr(move[1][0]+97) + str(abs(move[1][1]-7))))
                from_node = str(chr(move[0][0]+97) + str(abs(move[0][1]-7)))
                to_node = str(chr(move[1][0]+97) + str(abs(move[1][1]-7)))
                if(len(move) == 3):
                    self.mill = str(chr(move[2][0]+97) + str(abs(move[2][1]-7)))
                return board.move(from_node, to_node)
            except IndexError:
                return False

        # self.do_move(move, error_msg='AI failed to move stone, trying again...')
        self.do_move(move, error_msg=None)
        self.delay()

    def handle_fly(self, board):
        """Handle flying a stone on the board (in phase 'flying')."""
        def fly():
            try:
                ge = self.__new_state(board)
                move = ge.ai_move()
                move = ge.convert_to_seven_x_seven(list(move))
                #print("mf"+str(chr(move[0][0]+97) + str(abs(move[0][1]-7))))
                #print("mt"+str(chr(move[1][0]+97) + str(abs(move[1][1]-7))))
                from_node = str(chr(move[0][0]+97) + str(abs(move[0][1]-7)))
                to_node = str(chr(move[1][0]+97) + str(abs(move[1][1]-7)))
                if(len(move) == 3):
                    self.mill = str(chr(move[2][0]+97) + str(abs(move[2][1]-7)))
                return board.fly(from_node, to_node)
            except IndexError:
                return False

        self.do_move(fly, error_msg='AI failed to move stone, trying again...')
        self.delay()

    def handle_mill(self, board):
        """Handle when a mill was formed."""
        def mill():
            #__new_state(board)
            #removed_position = random.choice(board.nodes(self.opponent_color))
            #ge = self.__new_state(board)
            #move = ge.ai_move()
            #move = ge.convert_to_seven_x_seven(list(move))
            #print("mf"+str(move_from))
            #print("mt"+str(chr(move[0][0]+97) + str(abs(move[0][1]-7))))
            #print("mta"+str(move_take))
            #nkey = str(chr(move[0][0]+97) + str(abs(move[0][1]-7)))
            return board.remove(self.mill)

        self.do_move(
            mill, error_msg='AI failed to remove stone, trying again...')
        self.delay()
