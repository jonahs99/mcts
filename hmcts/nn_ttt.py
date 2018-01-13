import ttt
import nn
import numpy as np

def encode(state):
    inputs = np.zeros((18))
    inputs[0:9] = [ 1 if state.board[i] == state.turn else 0 for i in range(9) ]
    inputs[9:18] = [ 1 if state.board[i] == 3 - state.turn else 0 for i in range(9) ]

    return inputs

def pick_move(state, inputs, net, disp=False):
    probs = net.predict(inputs)
    if disp:
        print(probs)

    legal_moves = state.gen_moves()

    probs = [ probs[move.index] for move in legal_moves ]
    probs /= np.sum(probs)

    return np.random.choice(legal_moves, p = probs)

def play_game(net, disp=False):
    state = ttt.State()
    Xlist = []
    Olist = []
    while state.win_state() == -1:
        inputs = encode(state)
        move = pick_move(state, inputs, net, disp)
        state.make_move(move)

        target = np.zeros((9))
        target[move.index] = 1
        if state.turn == 1:
            Xlist.append( ( inputs, target ) )
        else:
            Olist.append( ( inputs, target ) )

        if disp:
            print(state)
    
    if state.win_state() == 0.5:
        return Xlist + Olist

    return Xlist if state.turn == 2 else Olist

net = nn.NeuralNet( (18, 12, 9) )

train_its = 0
for _ in range(100000):
    win_pattern = play_game(net)
    if win_pattern is not None:
        net.train(win_pattern, its=10)
        train_its += 1
    if train_its % 500 == 0:
        print(train_its)
        play_game(net, disp=True)
