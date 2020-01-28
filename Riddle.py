import random


class Riddle(object):
    def __init__(self):
        possible_riddles = [
            ('riddle', 'answer')
        ]

        self.riddle = possible_riddles[random.uniform(0, len(possible_riddles))]
