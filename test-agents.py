import agent
import human
import connect4

state = connect4.State()

agent2 = agent.Agent(connect4, time=1000)
agent1 = human.HumanAgent(connect4)

print(state)

while state.win_state() == -1:
    agent = (0, agent1, agent2)[state.turn]

    agent.think()
    move = agent.pick_move()

    state.make_move(move)
    agent1.apply_move(move)
    agent2.apply_move(move)

    print(state)