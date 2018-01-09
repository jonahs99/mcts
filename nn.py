import numpy as np
import math

_map = np.vectorize(lambda x, a, b, c, d: c + (x - a) / (b - a) * (d - c))
_sigmoid = np.vectorize(lambda x: 1 / (1 + math.exp(-x)))

class FFNN:

    def __init__(self, shape):
        self.shape = shape

        self.n = [ np.zeros((n, 1)) for n in shape ]
        self.w = [ _map(np.random.random((n, p)), 0, 1, -1, 1) for p,n in zip(shape, shape[1:]) ]
    def ff(self, inputs):
        self.n[0] = inputs
        for i in range(1, len(self.shape)):
            np.dot(self.w[i-1], self.n[i-1], self.n[i])
            self.n[i] = _sigmoid(self.n[i])
        return self.n[-1]