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
#print(visualbrackets[2])

matchbrackets = [[["A","B"],["C"]], [["A","B"], ["C","D"]], [["A","B"],["E"],["C","D"]], [["A","B"],["E"],["C","D"],["F"]], [["A","B"],["C","D"],["E","F"],["G"]], [["A","B"],["C","D"],["E","F"],["G", "H"]]]

def play(match):
    return match[0]

def matchOrganizer(brackets):
    while len(brackets[0]) != 1:
        for i in range(0, len(brackets)):
            if len(brackets[i]) == 2:
                x = play(brackets[i]) #the play function
                brackets[i].remove(x) #remove the loser
                print("Removed " + x) 
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
        print(brackets)
    #return tmp

print(matchbrackets[4])
matchOrganizer(matchbrackets[4])
#print(x)
#x = matchOrganizer(x)
#print(x)
#x = matchOrganizer(x)
#print(x)
