import agent
import human
import ttt
import connect4
import nash

print('Hello human!')
print('Which game?')

game = None
while game is None:
    game_input = input('(ttt, connect4, hex)')
    if game_input.startswith('t'):
        game = ttt
    elif game_input.startswith('c'):
        game = connect4
    elif game_input.startswith('h'):
        game = nash

state = game.State()

print('Player 1?')
agent1 = None
while agent1 is None:
    agent_input = input('(human, ai)')
    if agent_input.startswith('h'):
        agent1 = human.HumanAgent(game)
    elif agent_input.startswith('a'):
        while agent1 is None:
            time_input = input('time per move (sec)?')
            if int(time_input):
                agent1 = agent.Agent(game, time=int(time_input)*1000)

print('Player 2?')
agent2= None
while agent2 is None:
    agent_input = input('(human, ai)')
    if agent_input.startswith('h'):
        agent2 = human.HumanAgent(game)
    elif agent_input.startswith('a'):
        while agent2 is None:
            time_input = input('time per move (sec)?')
            if int(time_input):
                agent2 = agent.Agent(game, time=int(time_input)*1000)

print('Here we go!')
print('')
print(state)

while state.win_state() == -1:
    agent = (0, agent1, agent2)[state.turn]

    agent.think()
    move = agent.pick_move()

    state.make_move(move)
    agent1.apply_move(move)
    agent2.apply_move(move)

    print(state)