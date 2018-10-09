"""Game module."""

import random
import textwrap

from sepm import PieceColor as Color
from sepm.boards.nine_morris import NineMensMorrisBoard
from sepm.exceptions import FoundMillError, GameOver
from sepm.players.human import HumanPlayer
from sepm.players.random_ai import RandomAI


class Game(object):
    def __init__(self, board_cls=NineMensMorrisBoard,
                 max_time=1800, max_moves=50):
        """Initialize a new game instance."""
        self.board = board_cls(max_time=max_time, max_moves=max_moves)

    def add_player(self, name, color, ai_difficulty):
        """Add a new player."""
        if ai_difficulty:
            return self.add_random_ai(name, color)
        else:
            return self.add_human(name, color)

    def add_human(self, name, color):
        """Add a human player to the game."""
        player = HumanPlayer(name, color)
        self.board.add_player(color, player)
        return player

    def add_random_ai(self, name, color, delay=0.5):
        """Add an AI to the game."""
        player = RandomAI(name, color, delay=delay)
        self.board.add_player(color, player)
        return player

    def add_players(self, *players):
        """Add a new player to the game."""
        for player in players:
            self.board.add_player(player.color, player)
        return players

    def print_menu(self):
        """Print the menu."""
        print(textwrap.dedent('''
            Commands:
                q = Quit the game
                r = Resign the match
            '''))

    def center(self, msg, width=44):
        """Print centered text."""
        print(msg.center(width))

    def print_board(self):
        """Print the game board."""
        # Print score
        self.center('{} (B) vs {} (W)'.format(
            self.board.players[Color.Black],
            self.board.players[Color.White]
        ))
        self.center('{} - {}'.format(
            self.board.black_count,
            self.board.white_count
        ))

        # Print the actual game board
        self.center(str(self.board))

        # Print game board statistics
        players = self.board.players
        black = len(players[Color.Black].pieces)
        white = len(players[Color.White].pieces)

        self.center('Black stones left: {}'.format(black))
        self.center('White stones left: {}'.format(white))

    def run(self, start_color=None):
        """Start the game."""
        if not self.board.has_white_player or not self.board.has_black_player:
            raise Exception(
                'Please add a white and a black before starting the game')

        try:
            self.loop()
        except KeyboardInterrupt:
            print()
            raise GameOver(winner=None)

    def loop(self):
        """
        Main game loop.

        :raises GameOver: When the game is over.
        """
        while True:
            #print(self.board.nodes())
            self.board.change_turn()
            player = self.board.current

            self.print_board()
            self.print_menu()

            print("It's {name}'s ({color}) turn ({phase})!".format(
                name=self.board.current.name,
                color=self.board.current.color.value,
                phase=self.board.current.phase.value
            ))
        
            # Handle current player move
            try:
                if player.is_placing:
                    player.handle_place(self.board)
                elif player.is_moving:
                    player.handle_move(self.board)
                elif player.is_flying:
                    player.handle_fly(self.board)
            except FoundMillError:
                player.handle_mill(self.board)
