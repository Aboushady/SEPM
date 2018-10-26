
import unittest.mock
from unittest.mock import Mock
import builtins
from round_robin import RoundRobin


class TestRoundRobin():

    def test_matchups(self):
        """
        This function should set up the matchups from the given name list. If the number of names is odd a player named
        bye should be added.
        :return:
            A fourth player should be added and the matchups should not be equal at any time
        """

        names = ['first', 'second', 'third']
        self.names_len = len(names)
        res = RoundRobin.match_ups(self, names)
        assert res == [['first', 'second', 'third', 'bye'], ['first', 'bye', 'second', 'third'],
                       ['first', 'third', 'bye', 'second']]

    @staticmethod
    def test_gui():
        """
        This function should test for the format of the matchups by looking at the last round
        :return:
            the last matchup and round number
        """

        match_ups_ls = [['first', 'second', 'third', 'bye'],
                        ['first', 'bye', 'second', 'third'],
                        ['first', 'third', 'bye', 'second']]

        count = 0
        for i in match_ups_ls:
            count = count + 1
            temp_ls = zip(*[iter(i)] * 2)
            zipped_ls = list(temp_ls)
        assert zipped_ls == [('first', 'third'),('bye', 'second')] and count == 3

    def test_next_round(self):
        """
            Testing the input in the play function.
        :return:
        """
        match_ups_ls = [['first', 'second', 'third', 'bye'],
                        ['first', 'bye', 'second', 'third'],
                        ['first', 'third', 'bye', 'second']]

        m = Mock()
        m.side_effect = iter(['next', 'Next', 'quit', 'Quit'])

        with unittest.mock.patch.object(builtins, 'input', lambda x: m()):
            assert RoundRobin.next_round(self) == 'next' and RoundRobin.next_round(self) == 'quit'

#    #def test_play(self):
#       """
#             Testing the input in the play function.
#       :return:
#       """
#        #match_ups_ls = [['first', 'second', 'third', 'bye'],
#                        ['first', 'bye', 'second', 'third'],
#                        ['first', 'third', 'bye', 'second']]
#
#        m = Mock()
#        m.side_effect = iter(['play', 'Play', 'quit', 'Quit'])




