import nn
import math
import random
import numpy as np

shape = (1, 4, 2, 1)
net = nn.NeuralNet(shape)

inputs = [ np.random.random(1) for i in range(100) ]
outputs = [ np.array([math.sin(x)]) for x in inputs ]
#outputs = [ np.array([0.8]) for x in inputs ]
patterns = list(zip(inputs, outputs))

print('1')
net.train(patterns[:50])
print('2')
net.train(patterns[50:])