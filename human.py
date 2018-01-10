class HumanAgent:
    def __init__(self, game):
        self.game = game
        self.state = game.State()
    def apply_move(self, move):
        self.state.make_move(move)
    def think(self):
        pass
    def pick_move(self):
        legal = self.state.gen_moves()
        legal_notations = [move.__repr__() for move in legal]
        pick = None
        while True:
            print('Please choose a move:', legal)
            pick = input()
            match = list(filter(lambda move: pick.startswith(move.__repr__()) or move.__repr__().startswith(pick), legal))
            if len(match) == 1:
                return match[0]