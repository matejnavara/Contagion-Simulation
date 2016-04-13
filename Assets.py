__author__ = 'Matej'

import Utilities

HIGH = None
MED = None
LOW = None

class Assets:
    def __init__(self):
        self.load()

    def load(self):
        HIGH = Utilities.load_image('healthySuper.png')
        MED = Utilities.load_image('healthy1.png')
        LOW = Utilities.load_image('healthy2.png')