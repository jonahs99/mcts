import random

# a connect four board
class State:
    EMPTY = 0
    X = 1
    O = 2

    lines = []
    lines += [ [ (col, row), (col, row+1), (col, row+2), (col, row+3) ] for row in range(3) for col in range(7) ]
    lines += [ [ (col, row), (col+1, row), (col+2, row), (col+3, row) ] for row in range(6) for col in range(4) ]
    lines += [ [ (col, row), (col+1, row+1), (col+2, row+2), (col+3, row+3) ] for row in range(3) for col in range(4) ]
    lines += [ [ (col, row), (col-1, row+1), (col-2, row+2), (col-3, row+3) ] for row in range(3) for col in range(3, 7) ]

    def __init__(self):
        self.cols = [[ 0 for x in range(6) ] for x in range(7)]
        self.turn = State.X
    
    def gen_moves(self):
        moves = [Move(i) for i in filter(lambda col: State.EMPTY in self.cols[col], range(7))]
        return moves
        #moves = []
        #for col in cols:
        #    move = State(self.cols)
        #    r = 0
        #    while self.cols[col][r] != State.EMPTY:
        #        r += 1
        #    move.cols[col][r] = self.turn
        #    move.turn = State.X if self.turn == State.O else State.O
        #    moves.append(move)
        #return moves

    def make_move(self, move):
        r = 0
        while self.cols[move.index][r] != State.EMPTY:
            r += 1
        self.cols[move.index][r] = self.turn
        self.turn = 3 - self.turn

    def unmake_move(self, move):
        self.turn = 3 - self.turn
        r = 5
        while self.cols[move.index][r] == State.EMPTY:
            r -= 1
        self.cols[move.index][r] = State.EMPTY

    # returns -1 for not end of game, 1 for win, 0 for loss (from perspective of self.turn!!)
    def win_state(self):
        opponent = State.X if self.turn == State.O else State.O
        for line in State.lines:
            win = True
            lose = True
            for col, row in line:
                if self.cols[col][row] == State.EMPTY:
                    win = False
                    lose = False
                    break
                if self.cols[col][row] == self.turn:
                    lose = False
                elif self.cols[col][row] == opponent:
                    win = False
            if win:
                return 1
            if lose:
                return 0
        if any( State.EMPTY in col for col in self.cols ):
            return -1
        return 0.5

    def __repr__(self):
        sym = ['-', 'X', 'O']
        ret = ''
        for r in range(5, -1, -1):
            for c in range(7):
                ret += sym[self.cols[c][r]] + ' '
            ret += '\n'
        ret += '0 1 2 3 4 5 6\n'
        return ret

class Move:
    def __init__(self, index):
        self.index = index
    def __eq__(self, other):
        return self.index == other.index
    def __ne__(self, other):
        return self.index != other.index