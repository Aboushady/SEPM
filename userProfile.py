import sys
import random
import string



class UserProfiles:
	def __init__(self):
		# These Dictioanry should be initialized in the menu.py.
		self.user_prof_rr = {}
		self.user_prof_em = {}
		self.id_players = {}
		self.key_list = ["A", "B", "C", "D", "E", "F", "G", "H"]
		
                
	#User Info list in Round Robin Tournament.
	def setuserinfo_rr(self, name, points, sidecolor_rr):
		id_rr = self.random_char()
                #self.user_prof_rr[id_rr] = [name, points, sidecolor_rr]
                #self.setlistofplayers(id, listofplayers)

	#User Info list in Elimination Tournament [name, sidecolor, wins, loses].
	def setuserinfo_em(self, names, sidecolor_em, rounds):
                self.key_list = self.key_list[0:len(names)]
                for name in names:
                    id_em = self.random_char()
                    self.user_prof_em[id_em] = [name, sidecolor_em, rounds]

	#Associating each player in the Round Robin Tournament with the list players he didn't play against.
	def setlistofplayers(self, id, listofplayers):
		self.id_players[id] = [listofplayers]

	#Switching sides.
	def switchsides(self, id, tournamentmode):
		if tournamentmode == 'rr':
			if self.user_prof_rr[id][2] == 'b':
				self.user_prof_rr[id][2] = 'w'
			else:
				self.user_prof_rr[id][2] = 'b'
		else:
			if self.user_prof_em[id][1] == 'b':
				self.user_prof_em[id][1] = 'w'
			else:
				self.user_prof_em[id][1] = 'b'

	def random_char(self):  
            r = random.randrange(len(self.key_list))
            key = self.key_list[r]
            del self.key_list[r]
            return key
