import math
import time

import ttt
import connect4
import mcts
import plot

c = math.sqrt(2)
time_per_turn = 300
iteration_res = 10

state = connect4.State()
root = mcts.Node(None, None)
og = root

while root is not None:
    start_time = current_time()
    its = 0
    while current_time() - start_time < time_per_turn:
        for i in range(iteration_res):
            mcts.iterate(state, root, c)
        its += iteration_res

    print(its, 'iterations.')

    if len(root.children) == 0:
        win = state.win_state()
        if win == 1:
            print(state.turn, 'wins')
        elif win == 0.5:
            print('draw')
        elif win == 0:
            print(state.turn, 'loses')
        break

    sort = sorted(root.children, key = lambda node: node.n)
    best = sort[-1]

    state.make_move(best.move)
    root = best
    root.parent = None

    print(best)
    print(state)