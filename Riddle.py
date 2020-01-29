import random
from Text import Text


class Riddle(object):
    def __init__(self):
        possible_riddles = [
            ('riddle', 'answer')
        ]

        self.riddle = possible_riddles[random.randrange(0, len(possible_riddles))]
        self.text = Text(self.riddle[0], (0, 0), 'medium', False, (255, 255, 255))

    def render(self, screen):
        self.text.render(screen)
