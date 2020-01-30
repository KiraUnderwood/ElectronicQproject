import pickle
import os

from .queue import ElectronicQ


def pickle_the_q():
    if os.path.isfile('queue.pkl'):
        with open('queue.pkl', 'rb') as q:
            return pickle.load(q)
    else:
        return ElectronicQ()





