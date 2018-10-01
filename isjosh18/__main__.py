import argparse
import time
import random
import requests
import colorama


URL = 'https://hasjoshturned18yet.com/api.json'

color_dict = vars(colorama.Fore)
for color in ['BLACK', 'WHITE', 'LIGHTBLACK_EX', 'RESET']:
    del color_dict[color]
COLORS = list(color_dict.values())


class Balloon:
    shape = [x[4:] for x in '''
      .-'"'-.
     /C#XXXXX\\
    :X#XXXXXXX:
     \XXXXXXX/
      \XXXXX/
       `'p'`
         )
        (
         )
    '''.split('\n')][1:]
    width = max(len(x) for x in shape)

    def __init__(self, screen_width):
        self._screen_width = screen_width
        self._offset = random.randint(0, screen_width - Balloon.width)
        self._view = iter(Balloon.shape)
        self.color = random.choice(COLORS)

    def view(self):
        view = self._offset * ' ' + next(self._view)
        view += (self._screen_width - len(view)) * ' '
        return view


class Layer:

    def __init__(self, screen_width):
        self._view = list(' ' * screen_width)

    def add(self, view, color):
        new_view = []
        for old, new in zip(self._view, view):
            if new != ' ' and old == ' ':
                new_view.append(color + new)
            else:
                new_view.append(old)
        self._view = new_view

    def view(self):
        line = ''.join(self._view).replace('X', ' ')
        return line


def make_balloons(width, speed, frequency):
    balloons = []
    while True:
        if random.random() < frequency:
            balloons.append(Balloon(width))

        layer = Layer(width)
        new_balloons = []
        for balloon in balloons:
            try:
                layer.add(balloon.view(), balloon.color)
            except StopIteration:
                continue
            new_balloons.append(balloon)
        balloons = new_balloons
        print(random.choice(COLORS) + layer.view())
        time.sleep(1.0/speed)


def is_josh_18():
    try:
        res = requests.get(URL).json()
    except requests.ConnectionError as e:
        print('Can\'t connect: %s' % e)
        exit(1)
    return res['answer'] == 'yes'


def main():
    colorama.init()

    parser = argparse.ArgumentParser(description='Is Josh 18?')
    parser.add_argument(
        '--balloons', help='Add balloons', action='store_true')
    parser.add_argument(
        '-f', '--force', help='Force Josh to be 18', action='store_true')
    parser.add_argument(
        '--frequency', help='Balloon frequency', type=float, default=0.25)
    parser.add_argument(
        '--speed', help='Balloon speed', type=float, default=35)
    parser.add_argument(
        '--width', help='Screen width', type=int, default=80)
    args = parser.parse_args()

    yes = True if args.force else is_josh_18()

    if args.balloons:
        if not yes:
            print('Josh isn\'t 18 yet. Use -f/--force if you want balloons '
                  'anyway.')
            exit()
        try:
            make_balloons(args.width, args.speed, args.frequency)
        except KeyboardInterrupt:
            print('The party is over.')
        return

    print('Josh is ' + ('' if yes else 'NOT ') + '18.')
    exit(not yes)


if __name__ == '__main__':
    main()
