import time
import mcts

#7896

def _current_time():
    return round(time.time() * 1000)

class Agent:
    its_res = 10

    def __init__(self, game, time=None, iterations=None, c=2):
        if time is None and iterations is None:
            time = 1000

        self.c = c
        self.millis_to_think = time
        self.iterations = iterations

        self.state = game.State()
        self.root = mcts.Node(None, None)

    def reset(self):
        self.state = game.State()
        self.root = mcts.Node(None, None)

    def apply_move(self, move):
        self.state.make_move(move)
        match = list(filter(lambda node: node.move == move, self.root.children))
        if len(match):
            self.root = match[0]
            self.root.parent = None
        else:
            self.root = mcts.Node(None, move)

    def think(self):
        print('thinking...')
        if self.iterations is not None:
            for i in range(self.iterations):
                mcts.iterate(self.state, self.root, self.c)
        elif self.millis_to_think is not None:
            start_time = _current_time()
            its = 0
            while _current_time() - start_time < self.millis_to_think:
                for i in range(Agent.its_res):
                    mcts.iterate(self.state, self.root, self.c)
                its += Agent.its_res
            print('completed', its, 'iterations')

    def pick_move(self):
        best = sorted(self.root.children, key = lambda child: child.n)[-1]
        return best.move
