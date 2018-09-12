import sys
import random
import string


user_prof_rr = {}
user_prof_em = {}
id_players = {}

#User Info list in Round Robin Tournament.
def getuserinfo_rr(name, points, sidecolor_rr, listofplayers):
	id = random_char(4)
	global user_prof_rr = {id : [name, points, sidecolor_rr]}
	getlistofplayers(id, listofplayers)

#User Info list in Elimination Tournament.
def getuserinfo_em(name, sidecolor_em):
	id = random_char(4)
	global user_prof_em = {id : [name, sidecolor_em]}

#Associating each player in the Round Robin Tournament with the list players he didn't play against.
def getlistofplayers(id, listofplayers):
	global id_players = {id : listofplayers}

#Switching sides.
def switchsides(id, switchtocolor, tournamentmode):
	if tournamentmode == 'rr':
		user_prof_rr[id][2] = switchtocolor
	else:
		user_prof_em[id][1] = switchtocolor

def random_char(y):
	return ''.join(random.choice(string.ascii_letters) for x in range(y))
