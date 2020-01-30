import random
from Text import Text


class Riddle(object):
    def __init__(self):
        possible_riddles = [
            ('It reverses our breath', 'tree'),
            ('It winkles in your eye, very high in the sky', 'star'),
            ('He sits on a lap, just so he can nap', 'cat')
        ]

        self.riddle = possible_riddles[random.randrange(0, len(possible_riddles))]
        self.text = Text(self.riddle[0], (0, 0), 'medium', False, (255, 255, 255))

    def render(self, screen):
        self.text.render(screen)

    def check_solution(self, drawing_camera):
        return self.riddle[1] in drawing_camera.get_prediction()
