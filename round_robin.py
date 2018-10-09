import userProfile
import sys
import standings
from sepm import PieceColor
from sepm.exceptions import GameOver
from sepm.game import Game
from sepm.players.human import HumanPlayer
from sepm.players.random_ai import RandomAI

class RoundRobin:

    def __init__(self, user, names):
        self.usr = user
        self.standings_obj = standings.Standings()
        self.match_ups_ls = []
        self.plyrs_names = names
        self.names_len = len(names)

        self.player1 = self.player2 = ' '

    def rr_organizer(self):
        # for i in range(len(self.usr.id_players)/2):
        #     for key, value in self.usr.id_players.items():
        #         for j in range(0,len(value)):
        #             #Checking if they have the same colors.
        #             if self.usr.user_profiles[key][1] == self.usr.user_profiles[value[j]][1]:
        #                 continue
        #             else:
        self.match_ups_ls = self.match_ups(self.plyrs_names)
        print("This is fixtures" + str(self.match_ups_ls))
        self.gui(self.match_ups_ls)
        self.play(self.match_ups_ls)
        self.standings_obj.showstandings_after(self.usr, "rr")




    #Returns a list in the formate of [[(player1, player2),(player3, player4),(player5, player6)],....]
    def match_ups(self, names):
        #if the number of players is odd, add another dummy player called 'bye'.
        if self.names_len % 2:
            names.append('bye')
        rotation = list(names)  # copy the list
        fixtures = []
        for i in range(0, len(names) - 1):
            fixtures.append(rotation)
            rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]
        return fixtures

    def gui(self, match_ups_ls):
        count = 0
        for i in match_ups_ls:
            count = count+1
            temp_ls = zip(*[iter(i)] * 2)
            #This list loops through match_ups_ls, and contains at each iteration a sublist element from it.
            zipped_ls = list(temp_ls)

        #for i in range(0, len(match_ups_ls)):
            print ("Round :" + str(count) + "\n")
            for j in range(0, int(len(zipped_ls))):
                print(zipped_ls[j][0] + "\n" +
                      "----------------|\n"
                      "                |\n"
                      "                |\n"
                      "----------------|\n"
                      + zipped_ls[j][1]+ "\n \n")

    def play(self, match_ups_ls):
        x = " "
        winner_names_ls = []
        while x != "play":
            x = str.lower(input("Write 'play' to start, or 'quit' to exit the game: \n"))
            if x == "quit":
                sys.exit()
        #Calculate the number of rounds.

        rounds = 0
        if self.names_len % 2:
            rounds = self.names_len
        else:
            rounds = self.names_len - 1

        rounds_count = 0
        for i in match_ups_ls:
            if rounds_count < rounds:
                temp_ls = zip(*[iter(i)] * 2)
                zipped_ls = list(temp_ls)
                self.assign_rand_color(zipped_ls)
                self.update_gui(zipped_ls, rounds_count)
                #-Integration with GP.

                winner_names_ls = self.match_prep(zipped_ls)
                self.winner(winner_names_ls, rounds_count)

                #If this is the last round, don't call next_round().
                if rounds_count != rounds-1:
                    self.next_round()
                rounds_count = rounds_count + 1

    def assign_rand_color(self, zipped_ls):
        for i in range(0, len(zipped_ls)):
            for _, value in self.usr.user_profiles.items():
                if value[0] == zipped_ls[i][0]:
                    value[1] = 'B'
                if value[0] == zipped_ls[i][1]:
                    value[1] = 'W'

    def update_gui(self, zipped_ls, rounds_num):
        print("Round :" + str(rounds_num + 1))
        for i in range(0, len(zipped_ls)):
            print(zipped_ls[i][0] + "\n"
                  "----------------|\n"
                  "                |\n"
                  "                |\n"
                  "----------------|\n"
                  + zipped_ls[i][1] + "\n \n")


    def winner(self, winner_names_ls, rounds_count):

        #Get the winner based on the game, add points to the dict of the these players, and print them.

        #1-Statiscally assigning the winners, till the itegration with the actuall game.

        #2-Printings the winners
        print("The winners of round "+ str(rounds_count)+" are : \n" )
        # for i in range(0, len(zipped_ls)):
        #     print("-" + zipped_ls[i][0] + "\n")
        #     for key, value in self.usr.user_profiles.items():
        #         #3-Adding a point to each winner.
        #         if value[0] == zipped_ls[i][0]:
        #             value[3] = value[3] + 1
        if len(winner_names_ls) == 0:
            print('None\n')
        else:
            for i in range(0, len(winner_names_ls)):
                for _, value in self.usr.user_profiles.items():
                    if value[0] == winner_names_ls[i]:
                        value[3] = value[3] + 1
                print('*' + winner_names_ls[i] + '.\n')

    def next_round(self):
        x = " "
        while x != "next":
            x = str.lower(input("1- Write 'next' to proceed to the next round.\n"
                      "2- Write 'stat' to view the game's statistics.\n"                      
                      "3- Write 'quit' to quit. \n"))
            if x == "stat":
                self.standings_obj.showstandings_during(self.usr, "rr")

            if x == "quit":
                sys.exit()

    def match_prep(self, zipped_ls):
        winner_names_ls = []
        # 1-Loop through zipped_ls, for it contains the opponents of all matches at each round.
        for j in range(0, len(zipped_ls)):

            #Check if one of the opponents is the dummy player, if so then skip this match. (no points are given)
            if zipped_ls[j][0] == 'bye' or zipped_ls[j][1] == 'bye':
                continue
            # 2-Loop through userprofile, to get the colors of the players, and the last value of the userprofile,
            # dictionary, that says if it's a human or not.

            plyr_clr = plyr_clr_1 = is_human = is_human_1 = ' '
            for _, value in self.usr.user_profiles.items():
                if value[0] == zipped_ls[j][0]:
                    plyr_clr = value[1]
                    if plyr_clr == 'B':
                        plyr_clr = PieceColor.Black
                    else:
                        plyr_clr = PieceColor.White
                    is_human = value[4]
                if value[0] == zipped_ls[j][1]:
                    plyr_clr_1 = value[1]
                    is_human_1 = value[4]
                    if plyr_clr_1 == 'B':
                        plyr_clr_1 = PieceColor.Black
                    else:
                        plyr_clr_1 = PieceColor.White

            # if zipped_ls[j][0] == 'bye' or zipped_ls[j][1] == 'bye':
            #     if plyr_clr == ' ':
            #         if plyr_clr_1 == PieceColor.Black:
            #             plyr_clr = PieceColor.White
            #         else:
            #             plyr_clr = PieceColor.Black
            #     else:
            #         if plyr_clr == PieceColor.Black:
            #             plyr_clr_1 = PieceColor.White
            #         else:
            #             plyr_clr_1 = PieceColor.Black
            # Check if both players is human or AI.

            if is_human == 'none':
                self.player1 = HumanPlayer(zipped_ls[j][0], plyr_clr)

            else:
                self.player1 = RandomAI(zipped_ls[j][0], plyr_clr)

            if is_human_1 == 'none':
                self.player2 = HumanPlayer(zipped_ls[j][1], plyr_clr_1)
            else:
                self.player2 = RandomAI(zipped_ls[j][1], plyr_clr_1)

            name = self.start_match(self.player1, self.player2)
            x = ' '
            if name == ' ':
                while True:
                    x = str.lower(input("Write 'Yes' if you want to play again Or Enter to continue.\n"))
                    if x == 'yes':
                        name = self.start_match(self.player1, self.player2)
                        winner_names_ls.append(name)
                    else:
                        break
            else:
                winner_names_ls.append(name)

        return winner_names_ls

    def start_match(self, player1, player2):
        game = Game()
        game.add_players(player1, player2)
        x = name = ' '
        try:
            game.run()
        except GameOver as go:
            game.print_board()
            if go.winner is None:
                print("Game over! It's a draw.\n")
            else:
                name = go.winner.name
            x = str.lower(input("Write 'switch' to switch colors Or Press 'Enter' to continue. \n"))
            if x == 'swit':
                self.usr.switchsides(player1, player2)
        return name
