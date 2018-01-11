import numpy as np
from functools import reduce
import math

_map = np.vectorize(lambda x, a, b, c, d: c + (x - a) / (b - a) * (d - c))
_sigmoid = np.vectorize(lambda x: 1 / (1 + math.exp(-x)))
_sigmoid_derivative = np.vectorize(lambda x: x * (1.0 - x))

class FFNN:
    def __init__(self, shape):
        self.shape = shape
        self.a = [ np.zeros((n)) for n in shape ]
        self.o = [ np.zeros((n)) for n in shape ]
        self.b = [ _map(np.random.random((n)), 0, 1, -0.1, 0.1) for n in shape ]
        self.w = [ _map(np.random.random((nex, prev)), 0, 1, -0.1, 0.1) for prev, nex in zip(shape, shape[1:]) ]
        self.delta = [ np.zeros((n + 1)) for n in self.shape ]

    def ff(self, inputs):
        self.o[0] = inputs
        for i in range(1, len(self.shape)):
            self.a[i] = self.w[i-1].dot(self.o[i-1])# + self.b[i]
            self.o[i] = _sigmoid(self.a[i])
        return self.o[-1]

    def backpropogate(self, expected, layer = None):
        if layer is None:
            layer = len(self.shape) - 1
        if layer < 0:
            return
        if layer == len(self.shape) - 1:
            self.delta[layer] = (expected - self.o[layer]) * (_sigmoid_derivative(self.o[layer]))
        else:
            self.delta[layer] = self.w[layer].transpose().dot(self.delta[layer+1]) * (_sigmoid_derivative(self.o[layer]))
        self.backpropogate(expected, layer - 1)

    def update_weights(self, gamma):
        for layer in range(len(self.shape) - 1):
            o = self.o[layer]
            delta = self.delta[layer + 1]
            correction = gamma * np.outer(delta, o)
            self.w[layer] += correction

            self.b[layer] += gamma * self.delta[layer]
