from sepm.boards import GameBoard


class NineMensMorrisBoard(GameBoard):
    """Nine Men's Morris game board representation."""

    def _build_graph(self):
        """Build and returns graph with the nodes for the game board."""
        return self._load_graph_from_file('data/boards/nine_mens_morris.nodes')

    def __str__(self):
        """Render the game board as a string with the node pieces."""
        node_values = {
            key: '+' if node.piece is None else node.piece
            for key, node in self.state.items()
        }
        return '''
7  {a7} - - - - - - - - {d7} - - - - - - - - {g7}
   |                 |                 |
6  |     {b6} - - - - - {d6} - - - - - {f6}     |
   |     |           |           |     |
5  |     |     {c5} - - {d5} - - {e5}     |     |
   |     |     |           |     |     |
4  {a4} - - {b4} - - {c4}           {e4} - - {f4} - - {g4}
   |     |     |           |     |     |
3  |     |     {c3} - - {d3} - - {e3}     |     |
   |     |           |           |     |
2  |     {b2} - - - - - {d2} - - - - - {f2}     |
   |                 |                 |
1  {a1} - - - - - - - - {d1} - - - - - - - - {g1}
   a     b     c     d     e     f     g'''.strip().format(**node_values)

    def check_mill(self, position):
        """
        Check if a mill has occurred.

        :raises KeyError: On invalid board position
        :return: True if a mill was found, otherwise False.
        """
        if self.get_node(position) is None:
            return False

        count = self.count_nodes_direction

        horizontal = count(position, 'right')
        if horizontal == 3:
            return True
        if horizontal + count(position, 'left') - 1 == 3:
            return True

        vertical = count(position, 'up')
        if vertical == 3:
            return True
        if vertical + count(position, 'down') - 1 == 3:
            return True

        return False
