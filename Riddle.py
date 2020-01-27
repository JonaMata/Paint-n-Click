import random


class Riddle:
    def __init__(self):
        possible_riddles = [
            ('riddle', 'answer')
        ]

        self.riddle = possible_riddles[random.uniform(0, len(possible_riddles))]
