class HumanAgent:
    def __init__(self, game):
        self.game = game
        self.state = game.State()
    def apply_move(self, move):
        self.state.make_move(move)
    def think(self):
        pass
    def pick_move(self):
        legal = [move.index for move in self.state.gen_moves()]
        pick = None
        while pick not in legal:
            print('Please choose a move:', legal)
            pick = int(input())
        return self.game.Move(pick)