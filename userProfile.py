import sys

user_prof_RR = {}

def getUserInfo_RR(name, points, sideColor_RR):
	id = random_char(4)
	user_prof_RR[id] = [name, points, sideColor_RR]
	


user_prof_EM = {}
def getUserInfo_EM(name, sideColor_EM):
	 id = random_char(4)
	 user_prof_EM[id] = [name, sideColor_EM]
	
	

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))
