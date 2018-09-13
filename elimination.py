import random

visualbrackets =  [("AAAA            \n"
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

matchbrackets = [[["A","B"],["C"]], [["A","B"], ["C","D"]], [["A","B"],["E"],["C","D"]], [["A","B"],["E"],["C","D"],["F"]], [["A","B"],["C","D"],["E","F"],["G"]], [["A","B"],["C","D"],["E","F"],["G", "H"]]]

def play(match):
    r = random.random()
    if r < 0.5:
        return match[0]
    else:
        return match[1]

def eliminationOrganizer(brackets, size):
    nextWin = "W1W1"
    gui = visualbrackets[size-3]
    print(gui)
    while len(brackets[0]) != 1:
        for i in range(0, len(brackets)):
            if len(brackets[i]) == 2:
                x = play(brackets[i])       #the play function
                brackets[i].remove(x)       #remove the loser
                gui = updateGUI(nextWin, (brackets[i][0] + brackets[i][0] + brackets[i][0] +brackets[i][0]), gui) 
                if int(nextWin[1]) < size:  #decide where the winner of the next match will be on the gui
                    nextWin = nextWin.replace(nextWin[1], str(int(nextWin[1])+1))
                    #print(nextWin)
                print("Removed " + x)       #handle the stuff that's inbetween the matches here
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
        #print(gui)
        #print(tmp)
        #return tmp

def updateGUI(nextWin, winner, gui):
    return gui.replace(nextWin, winner)

s = 6
print(matchbrackets[s])
eliminationOrganizer(matchbrackets[s], s+3)
