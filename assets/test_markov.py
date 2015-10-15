from markov import Markov
from orientation import Orientation
from colors import Colors

map = [[1,2,3],
       [3,4,2],
       [3,2,1]]

markov = Markov(map, Orientation.WEST, "test")
markov.update(3)
markov.normalize()
markov.move()

for i in markov._p:
    print i

print markov