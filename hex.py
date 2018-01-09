n = 9

class State:
    EMPTY = 0
    X = 1
    O = 2

    def __init__(self):
        self.board = [[ 0 for x in range(n) ] for x in range(n)]
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
        # X connects top-down, Y connects left-right
        return 0.5

    def __repr__(self):
        sym = ['-', 'X', 'O']
        letter = [ chr(i + ord('a')) for i in range(26) ]
        ret = ''
        for r in range(n):
            ret += ' ' * r + letter[r] + ' '
            for c in range(n):
                ret += sym[self.board[r][c]] + ' '
            ret += '\n'
        ret += ' ' * (n + 2) + '0 1 2 3 4 5 6 7 8'
        return ret

class Move:
    def __init__(self, index):
        self.index = index
    def __eq__(self, other):
        return self.index == other.index
    def __ne__(self, other):
        return self.index != other.index

s = State()
print(s)