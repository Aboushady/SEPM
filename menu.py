import sys
import userProfile
import elimination
import round_robin


def quit(x):
    if(x.upper() == 'Q'):
        print('\nbye')
        sys.exit()

def main_menu():  
    option = 'X'
    while(option.upper() != 'T'):
        print('\n')
        print("           BestGame\n\n")
        print("Please select an option\n")

        print("[T] - Tournament\n")
        print('press q to quit\n')

        option = input("Please select an option: ")
        quit(option)
        print('\n')
    return(option)

#returns the amount of players specified by user, 3 <= players <= 8
def get_total_players():
        players = 0
        while(players < 3 or players > 8):
            players = input('Press q to quit or choose the total amount of players[ 3-8 ]: ')
            quit(players)
            if(players.isdigit() == False):
                players = 0
            else:
                players = int(players)

            print('\n')
        return(players)

#returns the amount of humans specified by user, 0 <= humans <= players
def get_human_players(players):
        humans = -1
        while (humans < 0 or humans > players):
            humans = input('Press q to quit or choose the amount of human players [0-%d]: '% players)
            quit(humans)
            if (humans.isdigit() == False):
                humans = -1
            else:
                humans = int(humans)

            print('\n')
        return(humans)

#returns a list of names that includes every participant(ai is called "com%d"), length(names) = players
def get_names_list(players, humans):
        i = 0
        names = []
        while (i < humans):
            name = input('Press q to quit or enter a 4 character name for player %d: ' % (i + 1))
            quit(name)
            if(len(name) == 4):
                names.append(name)
                i += 1
            else:
                print('Wrong input. Try again!')
            print('\n')
        ai = players-humans
        k = 0
        while(k < ai):
            names.append('com%dx' % k)
            k += 1
        return names


def start_menu():

    user = userProfile.UserProfiles()


    option = main_menu()

    if (option.upper() == 'T'):

        players = get_total_players()
        humans = get_human_players(players)
        names = get_names_list(players, humans)
        
        for x in names:
            print(x[:4])

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

        if tournament == 1:
            user.setuserinfo('rr', names)
            rr = round_robin.RoundRobin(user, names)
            rr.rr_organizer()
        else:
            user.setuserinfo('em', names, 'TBD')
            e = elimination.SingleElimination(user, len(names))
            e.eliminationOrganizer(len(names))

def main():

    start_menu()



main()
