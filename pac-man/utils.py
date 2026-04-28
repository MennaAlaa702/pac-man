import numpy as np

def vec(x, y):
    return np.array([x, y], dtype=float)

def distance(a, b):
    return np.linalg.norm(a - b)

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v