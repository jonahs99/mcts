import nn
import math
import random
import numpy as np

def train(nn, tgt, g):
    in_array = np.random.random(1)
    expected = tgt(in_array)
    delta = nn.ff(in_array) - expected
    nn.backpropogate(expected)
    nn.update_weights(g)
    return np.linalg.norm(delta)

target = lambda x: np.array([math.sin(x[0])])
#target = lambda x: np.array([0.5])
#target = lambda x: np.random.random(1)
#target = lambda x: np.array([1.0 - x[0]])

shape = (1, 10, 1)
gamma = 0.01

net = nn.FFNN(shape)

for i in range(10):
    E = 0
    for j in range(1000):
        E += train(net, target, gamma)
    print(E / 1000)