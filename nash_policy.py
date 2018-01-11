import nn
import nash
import numpy as np
from itertools import chain

class NashPolicy:
    def __init__(self):
        n = 9
        shape = (2 * n**2, n**2)
        self.nn = nn.FFNN(shape)
        self.n = n

        self.state = nash.State()
        self.in_array = np.array((2 * n**2))

    def reset(self):
        self.state = nash.State()

    def apply_move(self, move):
        self.state.make_move(move)

    def think(self):
        in_self = ( 1 if x == self.state.turn else 0 for x in self.state.board )
        in_opp = ( 1 if x == 3 - self.state.turn else 0 for x in self.state.board )
        self.in_array = np.fromiter(chain(in_self, in_opp), np.float, 2 * self.n ** 2)
        if (self.state.turn == 2):
            self.in_array = self.in_array.transpose()
            self.move_probs = self.nn.ff(self.in_array).reshape((self.n, self.n)).transpose().flatten()
        else:
            self.move_probs = self.nn.ff(self.in_array)

    def pick_move(self):
        legal = self.state.gen_moves()
        legal_dist = [ self.move_probs[move.index] for move in legal ]
        legal_dist /= np.sum(legal_dist)
        return np.random.choice(legal, 1, p = legal_dist)[0]

    def train(self, n_games):
        for i in range(n_games):
            self.state = nash.State()
            moves = []
            inputs = []
            while self.state.win_state() == -1:
                self.think()
                inputs.append(np.copy(self.in_array))
                move = self.pick_move()
                moves.append(move)
                self.state.make_move(move)
            # always the loser's turn at the end
            loser = self.state.turn
            start = 0 if loser == 2 else 1
            for mi in range(start, len(moves), 2):
                self.nn.ff(inputs[mi])
                target = np.zeros((self.n ** 2))
                target[moves[mi].index] = 1.0
                self.nn.backpropogate(target, 1)
                self.nn.update_weights(0.1)
        self.state = nash.State()
