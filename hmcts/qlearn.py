import ttt
import nn
import numpy as np
import random

def encode(state):
    inputs = np.zeros((18))
    inputs[0:9] = [ 1 if state.board[i] == state.turn else 0 for i in range(9) ]
    inputs[9:18] = [ 1 if state.board[i] == 3 - state.turn else 0 for i in range(9) ]

    return inputs

def get_move_value(net, move, state):
    state.make_move(move)
    value = net.predict(encode(state))
    state.unmake_move(move)
    return value

def play_through(net):
    epsilon = 0.2

    state = ttt.State()
    xmoves = []
    omoves = []

    while state.win_state() == -1:
        # pick a move
        legal_moves = state.gen_moves()
        move_values = [ get_move_value(net, legal_move, state) for legal_move in legal_moves ]

        if random.random() < epsilon:
            move = random.choice(legal_moves)
        else:
            move = sorted( zip(legal_moves, move_values), key=lambda z: z[1] )[-1][0]

        if state.turn == 1:
            xmoves.append(move)
        elif state.turn == 2:
            omoves.append(move)
        
        state.make_move(move)
    
    if state.win_state() == 0.5:
        return

    winner = 3 - state.turn
    if winner == 1:
        wmoves = xmoves
        lmoves = omoves
    elif winner == 2:
        wmoves = omoves
        lmoves = xmoves
    
    while len(lmoves) and len(wmoves):
        state.unmake_move(wmoves.pop())
        state.unmake_move(lmoves.pop())

####

value_net = nn.NeuralNet((18, 10, 1))

play_through(value_net)