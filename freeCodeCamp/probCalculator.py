import copy
import random
# Consider using the modules imported


class Hat():
    def __init__(self, **contents):
        self.contents = [k for k, v in contents.items() for _ in range(0, v)]

    def draw(self, ballNum):
        if ballNum >= len(self.contents):
            return self.contents
        else:
            return [self.contents.pop(random.randrange(len(self.contents))) for _ in range(ballNum)]


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    t = 0
    expected_balls = [k for k, v in expected_balls.items() for _ in range(v)]
    for _ in range(num_experiments):
        exp_hat = copy.deepcopy(hat)
        drawRes = exp_hat.draw(num_balls_drawn)
        t += 1 if len([drawRes.remove(x) for x in expected_balls if x in drawRes]) == len(expected_balls) else 0
    return t / num_experiments


hat = Hat(blue=3, red=2, green=6)

print(experiment(hat=hat,
                 expected_balls={"blue": 2, "green": 1},
                 num_balls_drawn=4,
                 num_experiments=1000))
