#Assuming that the dictionaries are Global, and the flag that says whether this is the standings are after the tournament,
#Or during it, and the type of the tournament is sent as a parameter.



class Standings:


        #def __init__(self, user):
        #       self.user = user

        def showstandings_during(self, user, tournament_type):
                if tournament_type == 'rr':
                        for key, value in user.user_prof_rr.items():
                                print("{first}-----{Second} \n".format(first=key, second=value[1]))
                else:
                        list = []
                        for key, value in user.user_prof_em.items(): #discuss about this approach.
                                # if value[2] > 0:
                                #   loser_dict[key] = value[2]
                                # else:
                                #   winner_dict[key] = value[2]
                                # print 'Winners                          Losers \n'
                                # print  winner_dict[key]+'             '+loser_dict[key]
                                list.append((value[2], value[0]))
                                #print(value[0] + '------' + value[2]
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
                
        def showstandings_after(self, tournament_type):
                if tournament_type == 'rr':
                        self.showstandings_during(tournament_type)
                        sorted_keys  = sorted(user.user_prof_rr, key=user.user_prof_rr.__getitem__)
                        sorted_values= sorted(user.user_prof_rr.value[2])
                        for i in range(1, 4):
                                print (i + ':' + sorted_keys[i-1] + '         ' + sorted_values[i-1])
#               else:
                        
                        

