import sys
import random
import string



class UserProfiles:
    def __init__(self):
        # These Dictioanry should be initialized in the menu.py.
        # Have one dictionary instead of two called user_profiles
        self.user_profiles= {}
        self.id_players = {}
        self.key_list = ["A", "B", "C", "D", "E", "F", "G", "H"]
        
    #User Info list in Elimination Tournament [tournamenttype, list of names, sidecolor, wins, loses].
    #sidecolor - 1 if black, 0 if white
    def setuserinfo(self, ttype, names, placement = '', points = 0):
                self.key_list = self.key_list[0:len(names)]
                for name in names:
                    id_em = self.random_char()
                    if(ord(id_em)%2 == 0):
                        sidecolor = True
                    else:
                        sidecolor = False
                        
                    if(ttype == 'em'):
                        self.user_profiles[id_em] = [name, sidecolor, placement]
                    elif(ttype == 'rr'):      
                        self.user_profiles[id_em] = [name, sidecolor, placement, points]
                        

    #Associating each player in the Round Robin Tournament with the list players he didn't play against.
    def setlistofplayers(self, id, listofplayers):
        self.id_players[id] = [listofplayers]

    #Switching sides.
    def switchsides(self, p1, p2):
                if(self.user_profiles[p1][1] != self.user_profiles[p2][1]):
                    self.user_profiles[p2][1] = not self.user_profiles[p2][1]
                    self.user_profiles[p1][1] = not self.user_profiles[p1][1]
                else:
                    r = random.random()
                    if(r < 0.5):
                        self.user_profiles[p1][1] = True
                        self.user_profiles[p2][1] = False
                    else:
                        self.user_profiles[p1][1] = False
                        self.user_profiles[p2][1] = True

    def random_char(self):  
            r = random.randrange(len(self.key_list))
            key = self.key_list[r]
            del self.key_list[r]
            return key
