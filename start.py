import curses



def init_screen(stdscr):
    curses.cbreak()
    curses.noecho()
    curses.nonl()
    curses.intrflush(False)
    stdscr.keypad(True)
    stdscr.refresh()



def start_menu(s):
    sh, sw = s.getmaxyx()
    menu = curses.newwin(sh, sw, 0, 0)
    menu.border()
    options = [0,0,0,0]
    option = 0
    choice = False



    while choice != True:

        options[option] = curses.A_STANDOUT

        menu.addstr(3, sw // 2 - 4, 'GameName')
        menu.addstr(sh // 2 - 1, sw // 2 - 3, 'VS game', options[0])
        menu.addstr(sh // 2, sw // 2 - 11, 'Round-robin tournament', options[1])
        menu.addstr(sh // 2 + 1, sw // 2 - 11, 'Elimination tournament', options[2])
        menu.addstr(sh // 2 + 2, sw // 2 - 2, 'Quit', options[3])
        menu.addstr(sh - 2, sw // 2 - 20, 'Valid Inputs: [w:Up] [s:Down] [k:select]')

        key_input = menu.getch()
        #select
        if key_input == ord('k'):
            choice = True
        #down
        elif key_input == ord('s'):
            options[option] = curses.A_NORMAL
            option = (option +1) % 4
        #up
        elif key_input == ord('w'):
            options[option] = curses.A_NORMAL
            option = (option -1) % 4
        menu.refresh()

    menu.clear()
    '''
    if(option == 0):
        #vs game
    elif(option == 1):
        #round robin tournament
    elif(option == 2):
        #elimination tournament
    elif(option == 3):
        #quit
        curses.endwin()
    '''



def main():
    # Initialize the screen
    s = curses.initscr()
    init_screen(s)
    start_menu(s)


main()
