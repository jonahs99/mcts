# Here, the state is a bit more complicated
# We hold a connection graph which modifies
#   as moves are made to analyze the win-
#   state efficiently

import random

n = 9

class State:
    EMPTY = 0
    X = 1
    O = 2

    # a set for each hex of connected indices
    # this could be more clear but it works...
    # note: this is a board shaped like \\ not //
    connections = [
        { nr * n + nc for nr,nc in {(r,c+1),(r-1,c+1),(r-1,c),(r,c-1),(r+1,c-1),(r+1,c)} if 0 <= nr < n and 0 <= nc < n }
        for r in range(n) for c in range(n) ]

    left_edge = { (r * n) for r in range(n) }
    right_edge = { (r * n + n - 1) for r in range(n) }
    top_edge = { (c) for c in range(n) }
    bottom_edge = { (c + n * (n - 1)) for c in range(n) }

    def __init__(self):
        self.board = [State.EMPTY for i in range(n*n)]
        self.turn = State.X
        self.node_grid = [GameNode(i) for i in range(n*n)]
        self.active_nodes = set()
        self.undo_stack = []
    
    def gen_moves(self):
        return [ Move(i) for i in filter(lambda x: self.board[x] == State.EMPTY, range(len(self.board))) ]

    def make_move(self, move):
        node = self.node_grid[move.index]
        node.activate(self.turn)
        self.active_nodes.add(node)

        undo = [(move.index, None, None)]
        self._attempt_merge(node, move.index, undo)
        self.undo_stack.append(undo)

        self.board[move.index] = self.turn
        self.turn = 3 - self.turn

    def unmake_move(self, move):
        self.turn = 3 - self.turn
        self.board[move.index] = State.EMPTY

        undo = self.undo_stack.pop()
        for i1, i2, n in reversed(undo):
            if i2 is None:
                self.active_nodes.remove(self.node_grid[i1])
            else:
                node = self.node_grid[i2]
                node.cons = n.cons
                node.left = n.left
                node.right = n.right
                node.top = n.top
                node.bottom = n.bottom
                self.active_nodes.add(self.node_grid[i1])

    # returns -1 for not end of game, 1 for win, 0 for loss (from perspective of self.turn!!)
    def win_state(self):
        for node in self.active_nodes:
            if node.color == State.X and node.left and node.right:
                return 1 if self.turn == State.X else 0
            if node.color == State.O and node.top and node.bottom:
                return 1 if self.turn == State.O else 0
        # Hex can't draw!
        return -1

    def _attempt_merge(self, node, index, undo):
        for other in self.active_nodes:
            if other is node:
                continue
            if node.color == other.color and index in other.cons:
                undo.append((node.index, other.index, other.copy()))
                self.active_nodes.remove(node)
                other.absorb(node)
                self._attempt_merge(other, index, undo)
                return

    def __repr__(self):
        sym = ['-', 'X', 'O']
        letter = [ chr(i + ord('a')) for i in range(26) ]
        ret = ''
        for r in range(n):
            ret += ' ' * r + letter[r] + ' '
            for c in range(n):
                ret += sym[self.board[r * n + c]] + ' '
            ret += '\n'
        ret += ' ' * (n + 2) + ''.join([str(i) + ' ' for i in range(n)])
        return ret

class Move:
    letter = [chr(i + ord('a')) for i in range(n)]
    number = [str(i) + ' ' for i in range(n)]

    def __init__(self, index):
        self.index = index
    def __eq__(self, other):
        return self.index == other.index
    def __ne__(self, other):
        return self.index != other.index
    def __repr__(self):
        return Move.letter[self.index // n] + Move.number[self.index % n]

class GameNode:
    def __init__(self, index):
        self.color = 0
        self.index = index
    def activate(self, color):
        self.color = color
        self.cons = State.connections[self.index]
        self.left = self.index in State.left_edge
        self.right = self.index in State.right_edge
        self.top = self.index in State.top_edge
        self.bottom = self.index in State.bottom_edge
    def absorb(self, node):
        self.cons = self.cons | node.cons
        self.left = self.left | node.left
        self.right = self.right | node.right
        self.top = self.top | node.top
        self.bottom = self.bottom | node.bottom
    def copy(self):
        node = GameNode(self.color)
        node.cons = self.cons.copy()
        node.left = self.left
        node.right = self.right
        node.top = self.top
        node.bottom = self.bottom
        return node

    def __repr__(self):
        rep = ('-', 'X', 'O')[self.color] + ' '
        if self.left:
            rep += 'L'
        if self.right:
            rep += 'R'
        if self.top:
            rep += 'T'
        if self.bottom:
            rep += 'B'
        rep += ', ' + self.cons.__repr__()
        return rep