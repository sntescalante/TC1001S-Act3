"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""


from random import choice
from turtle import *
from freegames import floor, vector


GHOST_SPEED = 10
TILE = 20

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)

aim = vector(5, 0)
pacman = vector(-40, -80)

ghosts = [
    [vector(-180, 160), vector(GHOST_SPEED, 0)],
    [vector(-180, -160), vector(0, GHOST_SPEED)],
    [vector(100, 160), vector(0, -GHOST_SPEED)],
    [vector(100, -160), vector(-GHOST_SPEED, 0)],
]

tiles = [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,
    0,1,0,0,0,1,1,0,1,0,0,0,1,0,1,0,0,0,1,0,
    0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,
    0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,
    0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,
    0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,
    0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,
    0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,
    0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,
    0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,
    0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,
    0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,
    0,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,
    0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,0,
    0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,0,1,1,0,
    0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,
    0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]
# fmt: on

def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for _ in range(4):
        path.forward(TILE)
        path.left(90)
    path.end_fill()

def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, TILE) + 200) / TILE
    y = (180 - floor(point.y, TILE)) / TILE
    return int(x + y * 20)

def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)
    if tiles[index] == 0:
        return False
    index = offset(point + 19)
    if tiles[index] == 0:
        return False
    return point.x % TILE == 0 or point.y % TILE == 0

def world():
    """Draw world using path."""
    bgcolor('black')
    path.color('blue')
    for index, tile in enumerate(tiles):
        if tile > 0:
            x = (index % 20) * TILE - 200
            y = 180 - (index // 20) * TILE
            square(x, y)
            if tile == 1:
                path.up()
                path.goto(x + TILE/2, y + TILE/2)
                path.dot(2, 'white')

def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])
    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * TILE - 200
        y = 180 - (index // 20) * TILE
        square(x, y)

    up()
    goto(pacman.x + TILE/2, pacman.y + TILE/2)
    dot(TILE, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(GHOST_SPEED, 0),
                vector(-GHOST_SPEED, 0),
                vector(0, GHOST_SPEED),
                vector(0, -GHOST_SPEED),
            ]
            if pacman.x > point.x and valid(point + vector(GHOST_SPEED, 0)):
                course.x, course.y = GHOST_SPEED, 0
            elif pacman.x < point.x and valid(point + vector(-GHOST_SPEED, 0)):
                course.x, course.y = -GHOST_SPEED, 0
            elif pacman.y > point.y and valid(point + vector(0, GHOST_SPEED)):
                course.x, course.y = 0, GHOST_SPEED
            elif pacman.y < point.y and valid(point + vector(0, -GHOST_SPEED)):
                course.x, course.y = 0, -GHOST_SPEED
            else:
                course.x, course.y = choice(options)

        up()
        goto(point.x + TILE/2, point.y + TILE/2)
        dot(TILE, 'red')

    update()

    for point, _ in ghosts:
        if abs(pacman - point) < TILE:
            return

    ontimer(move, 100)

def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
