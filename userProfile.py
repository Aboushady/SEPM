import sys
import random
import string

#These Dictioanry should be initialized in the menu.py.
user_prof_rr = {}
user_prof_em = {}
id_players = {}


class userprofiles:
	#User Info list in Round Robin Tournament.
	def getuserinfo_rr(self, name, points, sidecolor_rr, listofplayers):
		id = self.random_char(4)
		global user_prof_rr = {id : [name, points, sidecolor_rr]}
		self.getlistofplayers(id, listofplayers)

	#User Info list in Elimination Tournament.
	def getuserinfo_em(self, name, sidecolor_em):
		id = self.random_char(4)
		global user_prof_em = {id : [name, sidecolor_em]}

	#Associating each player in the Round Robin Tournament with the list players he didn't play against.
	def getlistofplayers(self, id, listofplayers):
		global id_players = {id : listofplayers}

	#Switching sides.
	def switchsides(self, id, switchtocolor, tournamentmode):
		if tournamentmode == 'rr':
			user_prof_rr[id][2] = switchtocolor
		else:
			user_prof_em[id][1] = switchtocolor

	def random_char(y):
		return ''.join(random.choice(string.ascii_letters) for x in range(y))
