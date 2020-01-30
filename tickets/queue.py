import pickle
from enum import Enum


class Services(Enum):
    OIL = 'oil'
    TIRES = 'tires'
    DIAG = 'diag'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ElectronicQ(metaclass=Singleton):

    def __init__(self):
        self.ticket_number = 0
        self.oil_time = 2
        self.tires_time = 5
        self.diagnostics_time = 30
        self.tickets_processing = {Services.OIL.value: [], Services.TIRES.value: [], Services.DIAG.value: []}
        self.current = 0

    def incr_tickt_no(self):
        self.ticket_number += 1
        return self.ticket_number

    def save_state(self):
        with open('queue.pkl', 'wb') as q:
            pickle.dump(self, q, pickle.HIGHEST_PROTOCOL)
