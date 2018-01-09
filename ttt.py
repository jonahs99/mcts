# a tic tac toe board
class State:
    EMPTY = 0
    X = 1
    O = 2

    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    def __init__(self):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.turn = State.X
    
    def gen_moves(self):
        return [ Move(i) for i in filter(lambda x: self.board[x] == State.EMPTY, range(len(self.board))) ]

    def make_move(self, move):
        self.board[move.index] = self.turn
        self.turn = 3 - self.turn

    def unmake_move(self, move):
        self.turn = 3 - self.turn
        self.board[move.index] = State.EMPTY

    # returns -1 for not end of game, 1 for win, 0 for loss (from perspective of self.turn!!)
    def win_state(self):
        opponent = State.X if self.turn == State.O else State.O
        for line in State.lines:
            if self.board[line[0]] == self.turn and self.board[line[1]] == self.turn and self.board[line[2]] == self.turn:
                return 1
            elif self.board[line[0]] == opponent and self.board[line[1]] == opponent and self.board[line[2]] == opponent:
                return 0
        for i in range(len(self.board)):
            if self.board[i] == State.EMPTY:
                return -1
        return 0.5

    def __repr__(self):
        sym = ['-', 'X', 'O']
        ret = ''
        for r in range(0, 3):
            for c in range(0, 3):
                ret += sym[self.board[r*3 + c]] + ' '
            ret += '\n'
        return ret

class Move:
    def __init__(self, index):
        self.index = index
    def __eq__(self, other):
        return self.index == other.index
    def __ne__(self, other):
        return self.index != other.index