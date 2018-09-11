import sys

def quit(x):
    if(x == 'q'):
        print('\nbye')
        sys.exit()

def start_menu():

    option = 0
    while(option != '1' and option != '2'):
        print('\n')
        print("           BestGame\n\n")
        print("Please select an option\n")
        print("1 - VS game\n")
        print("2 - Tournament\n")
        print('press q to quit\n')

        option = input("Please select an option: ")
        quit(option)
        print('\n')

    if option == '1':
        mode = 0
        while (mode < 1 or mode > 3):
            print('1 - player vs player\n')
            print('2 - player vs ai\n')
            print('3 - ai vs player\n')
            print('press q to quit\n')

            mode = input('choose a VS mode: ')
            quit(mode)

            if (mode.isdigit() == False):
                mode = 0
            else:
                mode = int(mode)
            print('\n')
            #Start a game

    elif option == '2':

        players = 0
        while(players < 3 or players > 8):

            players = input('Press q to quit or choose amount of players[ 3-8 ]: ')
            quit(players)
            if(players.isdigit() == False):
                players = 0
            else:
                players = int(players)

            print('\n')
        remaining = 8 - int(players)

        i = 0
        names = []
        while (i < players):
            name = input('Press q to quit or enter a 4 character name for player %d: ' % (i + 1))
            quit(name)
            if(len(name) == 4):
                names.append(name)
                i += 1
            else:
                print('Wrong input. Try again!')
            print('\n')

        if(remaining >= 1):
            ai = -1
            while(ai <= -1 or ai > remaining):
                ai = input('Press q to quit or choose amount of ai [ 0 - %d ]: ' % remaining)
                quit(ai)
                if (ai.isdigit() == False):
                    ai = -1
                else:
                    ai = int(ai)
                print('\n')

        k = 0
        while(k < remaining):
            names.append('ai')
            k += 1

        tournament = 0
        while (tournament < 1 or tournament > 2):
            print('1 - round-robin\n')
            print('2 - elimination\n')
            print('press q to quit\n')
            tournament = input('choose a tournament mode: ')
            quit(tournament)
            if (tournament.isdigit() == False):
                tournament = 0
            else:
                tournament = int(tournament)
            print('\n')

        #here we should call the different game modes by using the parameter tournament and the names list




def main():

    start_menu()



main()