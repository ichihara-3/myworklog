# Usage:
# python3 life-game.py
#
# <C-c> to exit
#

import copy
import os
import random
import sys
import time
from os import path


class LifeGame(object):

    DEAD = "□"
    ALIVE = "■"

    @staticmethod
    def random_board(width, height):
        return LifeGame([
            [random.choice([LifeGame.DEAD, LifeGame.ALIVE]) for x in range(width)]
             for y in range(height)
        ])

    def __init__(self, rows):
        self._rows = rows
        self._height = len(rows)
        self._width = len(rows[0])

    def dump(self):
        return "\n".join(["".join(row) for row in self._rows])

    def cell(self, x, y):
        x = (x + self._width) % self._width
        y = (y + self._height) % self._height
        return self._rows[y][x]

    def neighbors(self, x, y):
        cell = self.cell
        return [
            cell(x-1, y-1),
            cell(x-1, y),
            cell(x-1, y+1),
            cell(x, y-1),
            cell(x, y+1),
            cell(x+1, y-1),
            cell(x+1, y),
            cell(x+1, y+1)
        ]

    def density(self, x, y):
        return sum(map(self.is_alive, self.neighbors(x, y)))
        #return len(list(filter(self.is_alive, self.neighbors(x, y))))

    def is_alive(self, value):
        return value == self.ALIVE 

    def iterate(self):
        for y in range(len(self._rows)):
            for x in range(len(self._rows[y])):
                yield (x, y)

    def next_state(self, x, y):
        density = self.density(x, y)
        current_state = self.cell(x, y)

        if current_state == self.DEAD and density == 3:
            return self.ALIVE
        if current_state == self.ALIVE and density in (2, 3):
            return self.ALIVE
        if current_state == self.ALIVE and density <= 1:
            return self.DEAD
        if current_state == self.ALIVE and density >= 4:
            return self.DEAD
        return current_state

    def update(self):
        new_rows = copy.deepcopy(self._rows)
        for (x, y) in self.iterate():
            new_rows[y][x] = self.next_state(x, y)
        self._rows = new_rows
            
def main():
    try:
        life_game = LifeGame.random_board(64, 32)
        while True:
            os.system("clear")
            print(life_game.dump(), end='')
            time.sleep(0.1)
            life_game.update()
    except KeyboardInterrupt:
        print('\n', 'exit...')
        sys.exit(0)


if __name__ == "__main__":
    main()

