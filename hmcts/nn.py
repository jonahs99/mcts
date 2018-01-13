import math
import numpy as np

class NeuralNet:
    def __init__(self, shape):
        self.activation = lambda x: 1 / (1 + math.exp(-x))
        self.dactivation = lambda x: x * (1 - x)
        self.vactivation = np.vectorize(self.activation)
        self.vdactivation = np.vectorize(self.dactivation)

        self.shape = shape
        self.n_layers = len(shape)

        self.outputs = [ np.zeros(n) for n in shape ]

        self.weights = [ np.ones((nex, prev)) * 0.5 for prev,nex in zip(shape, shape[1:]) ]
        self.biases = [ np.zeros((n)) for n in shape[1:] ]
    
    def _feed_forward(self, inputs):
        if len(inputs) != self.shape[0]:
            raise(ValueError, 'Input array is wrong size.')

        self.outputs[0] = np.array(inputs)

        for layer in range(1, self.n_layers):
            W = self.weights[layer - 1]
            o = self.outputs[layer - 1]
            b = self.biases[layer - 1]

            self.outputs[layer] = self.vactivation(np.dot(W , o) + b)
        
        return self.outputs[-1]

    def _back_propogate(self, targets, gamma):
        if len(targets) != self.shape[-1]:
            raise(ValueError, 'Target array is wrong size.')
        
        deltas = [ np.zeros(n) for n in self.shape ]
        
        output_error = self.outputs[-1] - targets
        deltas[-1] = self.dactivation(self.outputs[-1]) * output_error

        for layer in range(self.n_layers - 2, -1, -1):
            W = self.weights[layer]
            delta_ = deltas[layer + 1]
            error = W.T.dot(delta_)
            deltas[layer] = error * self.vdactivation(self.outputs[layer])

            change = np.outer(delta_, self.outputs[layer])
            W -= change * gamma
            self.biases[layer] -= delta_ * gamma
        
        return np.linalg.norm(output_error) ** 2
    
    def train(self, patterns, its = 1000, gamma = 0.01, decay = 0.8):
        for _ in range(its):
            E = 0
            for i, p in enumerate(reversed(patterns)):
                self._feed_forward(p[0])
                E += self._back_propogate(p[1], gamma * decay**i)
            E /= len(patterns)
            #if i % (its // 10) == 0:
            #    print(E)
    
    def predict(self, inputs):
        return self._feed_forward(inputs)