import menu
import pytest
import unittest.mock
from unittest.mock import Mock
import builtins

class TestMenu():
    
    def test_quit(self):
        menu.quit('qq')
        with pytest.raises(SystemExit):
            menu.quit('q')

    def test_main_menu(self):
        m = Mock()
        m.side_effect = iter(['1', '', 'aa', 'B', 'T'])
        with unittest.mock.patch.object(builtins, 'input', lambda x: m()):
            assert menu.main_menu() == 'T'

    def test_start_menu(self):
        m = Mock()
        m.side_effect = iter(['T', '8', '4', 'asdf', 'ASDF', '1234', '  h1', '0', 'q'])
        with unittest.mock.patch.object(builtins, 'input', lambda x: m()):
            with pytest.raises(SystemExit):
                menu.start_menu()

    def test_get_total_players(self):
        m = Mock()
        m.side_effect = iter(['-1', '0', '10', '9', 'a', '', '8'])
        with unittest.mock.patch.object(builtins, 'input', lambda x: m()):
            assert menu.get_total_players() == 8
          
    def test_get_human_players(self):
        m = Mock()
        m.side_effect = iter(['-1','10', '9', 'a', '', '0'])
        with unittest.mock.patch.object(builtins, 'input', lambda x: m()):
            assert menu.get_human_players(8) == 0

    def test_get_names_list(self):
        m = Mock()
        m.side_effect = iter(['asdf', 'ASDF', 'sa3kjsdk', '', '1234', 'ssh1'])
        with unittest.mock.patch.object(builtins, 'input', lambda x: m()):
            assert menu.get_names_list(8, 4) == ['asdf', 'ASDF', '1234', 'ssh1', 'com0', 'com1', 'com2', 'com3']
        
