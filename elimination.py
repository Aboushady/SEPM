import random
import sys
import standings

class SingleElimination:
        def __init__(self, users, size):
            self.size = size
            self.gui =  [("AAAA            \n"
                    "-------         \n"
                    "       | W1W1   \n"
                    "       |------- \n"
                    "BBBB   |       |\n"
                    "-------        | W2W2  \n"
                    "               |-------\n"
                    "               |       \n"
                    "         CCCC  |\n"
                    "        -------   "),
                    ("AAAA             \n"
                    "-------          \n"
                    "       | W1W1    \n"
                    "       |-------  \n"
                    "BBBB   |       | \n"
                    "-------        | W3W3  \n"
                    "CCCC           |-------\n"
                    "-------        |       \n"
                    "       | W2W2  | \n"
                    "       |-------  \n"
                    "DDDD   |         \n"
                    "-------            "),
                    (
                    "         EEEE                  \n"
                    "        -------                \n"
                    "               |               \n"
                    "               | W3W3          \n"
                    "AAAA           |-------        \n"
                    "-------        |       |       \n"
                    "       | W1W1  |       |       \n"
                    "       |-------        |       \n"
                    "BBBB   |               |       \n"
                    "-------                |       \n"
                    "                       | W4W4  \n"
                    "        CCCC           |-------\n"
                    "        -------        |       \n"
                    "               | W2W2  |       \n"
                    "               |-------        \n"
                    "        DDDD   |               \n"
                    "        -------                \n"),
                    (
                    "         EEEE           \n"
                    "        -------         \n"
                    "               |        \n"
                    "               | W3W3   \n"
                    "AAAA           |------- \n"
                    "-------        |       |\n"
                    "       | W1W1  |       |\n"
                    "       |-------        |\n"
                    "BBBB   |               |\n"
                    "-------                |\n"
                    "                       | W5W5  \n"
                    "CCCC                   |-------\n"
                    "-------                |\n"
                    "       | W2W2          |\n"
                    "       |-------        |\n"
                    "DDDD   |       |       |\n"
                    "-------        | W4W4  |\n"
                    "               |-------\n"
                    "               |       \n"
                    "         FFFF  |       \n"
                    "        -------          "),
                    (
                    "AAAA             \n"
                    "-------          \n"
                    "       | W1W1    \n"
                    "       |-------  \n"
                    "BBBB   |       | \n"
                    "-------        | W4W4  \n"
                    "CCCC           |------- \n"
                    "-------        |       |\n"
                    "       | W2W2  |       |\n"
                    "       |-------        |\n"
                    "DDDD   |               |\n"
                    "-------                |\n"
                    "                       | W6W6  \n"
                    "EEEE                   |-------\n"
                    "-------                |\n"
                    "       | W3W3          |\n"
                    "       |-------        |\n"
                    "FFFF   |       |       |\n"
                    "-------        | W5W5  |\n"
                    "               |-------\n"
                    "               |       \n"
                    "         GGGG  |       \n"
                    "        -------          "),
                    (
                    "AAAA             \n"
                    "-------          \n"
                    "       | W1W1    \n"
                    "       |-------  \n"
                    "BBBB   |       | \n"
                    "-------        | W5W5  \n"
                    "CCCC           |------- \n"
                    "-------        |       |\n"
                    "       | W2W2  |       |\n"
                    "       |-------        |\n"
                    "DDDD   |               |\n"
                    "-------                |\n"
                    "                       | W7W7  \n"
                    "EEEE                   |-------\n"
                    "-------                |\n"
                    "       | W3W3          |\n"
                    "       |-------        |\n"
                    "FFFF   |       |       |\n"
                    "-------        | W6W6  |\n"
                    "GGGG           |-------\n"
                    "-------        |       \n"
                    "       | W4W4  |       \n"
                    "       |-------        \n"
                    "HHHH   |               \n"
                    "-------                  ")]

            self.matchbrackets = [[["A","B"],["C"]], [["A","B"], ["C","D"]], [["A","B"],["E"],["C","D"]], [["A","B"],["E"],["C","D"],["F"]], [["A","B"],["C","D"],["E","F"],["G"]], [["A","B"],["C","D"],["E","F"],["G", "H"]]]
            self.users = users
            
        def play(self, match):
            r = random.random()
            if r < 0.5:
                return match[0]
            if r > 0.9:
                return " "
            else:
                return match[1]

        def eliminationOrganizer(self, size = 3):
            brackets = self.matchbrackets[size - 3]
            nextWin = "W1W1"
            self.gui = self.gui[size-3]
            self.createGUI()
            standing = standings.Standings()
            while len(brackets[0]) != 1:
                for i in range(0, len(brackets)):
                    if len(brackets[i]) == 2:
                        print(self.gui)
                        print("Next match: " + self.users.user_prof_em[brackets[i][0]][0] + " vs " + self.users.user_prof_em[brackets[i][1]][0])
                        self.nextMatch()
                        x = self.play(brackets[i])       #the play function
                        x = self.checkWinner(brackets[i], x)
                        self.users.user_prof_em[x][2] = str(len(brackets)+1)
                        print("Place :" + str(len(brackets)+1))
                        brackets[i].remove(x)       #remove the loser
                        print("The Winner is: " + self.users.user_prof_em[brackets[i][0]][0])
                        self.updateGUI(nextWin, self.users.user_prof_em[brackets[i][0]][0]) 
                        if int(nextWin[1]) < size:  #decide where the winner of the next match will be on the gui
                            nextWin = nextWin.replace(nextWin[1], str(int(nextWin[1])+1))
                            #print(nextWin)
                        #print("Removed " + x)       #handle the stuff that's inbetween the matches here
                tmp = []
                while len(brackets) != 0:
                    if len(brackets) != 1:
                        tmp.append([brackets[0][0],brackets[1][0]])
                        del brackets[0]
                        del brackets[0]
                    else:
                        tmp.append([brackets[0][0]])
                        del brackets[0]
                brackets = tmp
            #self.updateGUI(nextWin, self.users.user_prof_em[brackets[i][0]][0])
            print(self.gui)
            self.users.user_prof_em[brackets[0][0]][2] = '1'
            #print(tmp)
            #return tmp
            standing.showstandings_during(self.users, 'no')

        def updateGUI(self, nextWin, winner):
            self.gui = self.gui.replace(nextWin, winner)

        def createGUI(self):
            for key, value in self.users.user_prof_em.items():
                #print(key+key+key+key+'----'+value[0])
                self.gui = self.gui.replace(key+key+key+key, value[0])
                
        def nextMatch(self):
            x = " "
            while x != "next":
                x = input("Write 'next' to proceed to the next match and 'quit' to quit: ")
                if x == "quit":
                    sys.exit()
        def checkWinner(self, players, loser):
            if loser != " ":
                return loser
            while loser == " ":
                x = input("Draw! Write 'rematch' to play again or 'random' to pick a random winner")
                if x == 'rematch':
                    loser = self.play(players)
                if x == 'random':
                    loser = players[0]
            loser = self.checkWinner(players, loser)
            return loser
#s = 5
#print(matchbrackets[s])
#eliminationOrganizer(matchbrackets[s], s+3)
