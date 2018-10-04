import userProfile
import sys
import standings
class RoundRobin:

    def __init__(self, user, names):
        self.usr = user
        self.standings_obj = standings.Standings()
        self.match_ups_ls = []
        self.plyrs_names = names
        self.names_len = len(names)

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
                self.winner(zipped_ls, rounds_count)

                #If this is the last round, don't call next_round().
                if rounds_count != rounds-1:
                    self.next_round()
                rounds_count = rounds_count + 1

    def assign_rand_color(self, zipped_ls):
        for i in range(0, len(zipped_ls)):
            for key, value in self.usr.user_profiles.items():
                if value[0] == zipped_ls[i][0] :
                    value[1] = 'b'
                if value[0] == zipped_ls[i][1]:
                    value[1] = 'w'

    def update_gui(self, zipped_ls, rounds_num):
        print("Round :" + str(rounds_num + 1))
        for i in range(0, len(zipped_ls)):
            print(zipped_ls[i][0] + "\n"
                  "----------------|\n"
                  "                |\n"
                  "                |\n"
                  "----------------|\n"
                  + zipped_ls[i][1] + "\n \n")


    def winner(self, zipped_ls, rounds_count):

        #Get the winner based on the game, add points to the dict of the these players, and print them.

        #1-Statiscally assigning the winners, till the itegration with the actuall game.

        #2-Printings the winners
        print("The winners of round "+ str(rounds_count)+" are : \n" )
        for i in range(0, len(zipped_ls)):
            print("-" + zipped_ls[i][0] + "\n")
            for key, value in self.usr.user_profiles.items():
                #3-Adding a point to each winner.
                if value[0] == zipped_ls[i][0]:
                    value[3] = value[3] + 1

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
