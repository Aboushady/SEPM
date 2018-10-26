from elimination import SingleElimination
import pytest
import unittest.mock
from unittest.mock import Mock
import builtins


class TestSingleElimination():

    def test_nextMatch(self):
        m = Mock()
        m.side_effect = iter(['d', '', 'next'])
        with unittest.mock.patch.object(builtins, 'input', lambda x: m()):
            SingleElimination.nextMatch(self)

        m.side_effect = iter(['d', '', 'quit'])
        with unittest.mock.patch.object(builtins, 'input', lambda x: m()):
            with pytest.raises(SystemExit):
                SingleElimination.nextMatch(self)
