import userProfile

class RoundRobin:

    def __init__(self):
        self.usr = userProfile.UserProfiles()
        self.match_ups = []
    def rr_tournament(self):
        for i in range(len(self.usr.id_players)/2):
            for key, value in self.usr.id_players.items():
                for j in range(0,len(value)):
                    if self.usr.user_profiles[key][1] == self.usr.user_profiles[value[j]][1]:
                        continue
                    else:

    def create_gui(self):
        for i in range(0, len(self.match_ups)):
            print(self.match_ups[i][0] +
                  "|----------------|          "                   
                  "|----------------|  Winner  "
                  "|----------------|----------"
                  "|----------------|          "
                  + self.match_ups[i][1]+ "\n")

