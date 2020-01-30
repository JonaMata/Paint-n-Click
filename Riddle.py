import random
from Text import Text


class Riddle(object):
    def __init__(self):
        possible_riddles = [
            ("Born underground, raised by the sun, a host for the living, caterer of fun.", 'tree'),
            ("What has roots that shows, up, up, up it goes but yet it never grows?", 'mountain'),
            ("I twinkle but I’m not an eye", 'star'),
            ("He sits on a lap, just so he can nap", 'cat'),
            ("I can fly, but I have no wings, I can cry, but I have no eyes", 'cloud'),
            ("drivers run me all the time if they are caught they get a fine what am I ?", 'stop_sign'),
            ("I am alive without breath. I am never thirsty but always drinking.", 'fish')
        ]

        self.riddle = possible_riddles[random.randrange(0, len(possible_riddles))]
        self.riddle = possible_riddles[3]
        self.text = Text(self.riddle[0], (0, 0), 'small', False, (255, 255, 255))

    def render(self, screen):
        self.text.render(screen)

    def check_solution(self, drawing_camera):
        return self.riddle[1] in drawing_camera.get_prediction()
