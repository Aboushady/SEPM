#Assuming that the dictionaries are Global, and the flag that says whether this is the standings are after the tournament,
#Or during it, and the type of the tournament is sent as a parameter.

import operator

class Standings:


        #def __init__(self, user):
        #       self.user = user

        def showstandings_during(self, user, tournament_type):
                #Implent rr
                if tournament_type == 'rr':
                        sorted_ls = sorted(user.user_profiles.items(), key=operator.itemgetter(1))
                        print(sorted_ls)
                        for i in reversed(sorted_ls):
                                print(str(i[1][0]) + '--------' + str(i[1][3]) + '\n')

                elif tournament_type == 'em':
                        list = []
                        for key, value in user.user_profiles.items(): 
                                list.append((value[2], value[0]))
                                
                        list.sort(key=self.sortS)
                        print("NAME----PLACEMENT\n")
                        for i, value in enumerate(list):
                                if len(list) == 5 and i == 4:
                                        print(value[1] + '---- 5')
                                elif len(list) > 3 and (list[i][0] == '3' or list[i][0] == '4'):
                                        print(value[1] + '---- 3-4\n')
                                elif len(list) > 4 and list[i][0] != 'TBD' and int(list[i][0]) > 4:
                                        print(value[1] + '---- 5-'+ str(len(list))+'\n')
                                else:
                                        print(list[i][1] + '---- ' + list[i][0]+'\n')

        def sortS(self, s):
                return int(s[0])
                
        def showstandings_after(self, user, tournament_type):
                if tournament_type == 'rr':
                        sorted_ls = sorted(user.user_profiles.items(), key=operator.itemgetter(1))
                        count = 0
                        for i in reversed(sorted_ls):
                                count = count + 1
                                print(str(count) + ':- ' + str(i[1][0]) + '--------' + str(
                                        i[1][3]) + '\n')
                                if count == 3:
                                        break
#               else:
                        
                        

