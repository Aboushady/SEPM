from collections import namedtuple  # This is an easy way to implement an enum.
COLORS = namedtuple("COLORS", "empty black white")
BOARD_SLOT = COLORS(0, 1, 2)

MOVES = namedtuple("MOVES", "not_taking placement_phase")
MOVE_PROPERTY = MOVES((-1, -1, -1), (-1, -1, -1))

PHASES = namedtuple("PHASES", "placement_phase movement_phase end_phase")
PHASE_PROPERTY = PHASES(0, 1, 2)
