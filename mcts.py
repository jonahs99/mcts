from math import sqrt, log, inf
import random

def iterate(state, root, c):
    selected = _select(state, root, root.n, c)
    # state is leaf
    expanded = _expand(state, selected)
    # state is leaf
    win, turn = _rollout(state, random.choice)
    _update(state, expanded, win, turn)
    # state is root

class Node:
    def __init__(self, parent, move):
        self.move = move

        self.parent = parent
        self.children = []

        self.w = 0
        self.n = 0
    def uct(self, c, N):
        if self.n == 0:
            return inf
        return self.w / self.n + c * sqrt(log(N) / self.n)
    def __repr__(self):
        ret = str(self.w) + '/' + str(self.n) + '\n'
        return ret

def print_tree(node, indent):
    print('| ' * indent, node.w, '/', node.n)
    for child in node.children:
        print_tree(child, indent + 1)

# recurse to a leaf node
def _select(state, node, N, c):
    if len(node.children) == 0:
        return node

    best = sorted(node.children, key = lambda node: node.uct(c, N))[-1]
    state.make_move(best.move)
    return _select(state, best, N, c)

def _expand(state, node):
    if state.win_state() != -1:
        return node
    for move in state.gen_moves():
        child = Node(node, move)
        node.children.append(child)
    child = random.choice(node.children)
    state.make_move(child.move)
    return child

def _rollout(state, policy):
    win = state.win_state()
    if win != -1:
        return (win, state.turn)
    
    move = policy(state.gen_moves())
    state.make_move(move)
    move_rollout = _rollout(state, policy)
    state.unmake_move(move)
    return move_rollout

def _update(state, node, win, turn):
    w = 1 - win if state.turn == turn else win
    node.w += w
    node.n += 1
    if node.parent is not None:
        state.unmake_move(node.move)
        _update(state, node.parent, win, turn)