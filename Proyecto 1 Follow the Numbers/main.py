import pgzrun
from random import randint
from pgzero.actor import Actor

# Variables de juego
WIDTH = 500
HEIGHT = 400

dots = []
lines = []

next_dot = 0
number_of_dots = 5


def create_dots():
    for dot in range(0, number_of_dots):
        actor = Actor("dot")
        actor.pos = randint(20, WIDTH - 20), randint(20, HEIGHT - 20)
        dots.append(actor)


def draw():
    screen.fill("black")
    # Etiqueta de los puntos
    number = 1
    for dot in dots:
        # Ubica el texto de la etiqueta encima del punto
        screen.draw.text(str(number), (dot.pos[0], dot.pos[1] + 12))
        dot.draw()
        number += 1

    for line in lines:
        screen.draw.line(line[0], line[1], (255, 255, 0))


def on_mouse_down(pos):
    global next_dot, lines, dots

    # Comprueba si se hizo click en el siguiente punto
    if dots[next_dot].collidepoint(pos):
        # Comprueba si se habia dado click al primer punto
        if next_dot:
            lines.append((dots[next_dot - 1].pos, dots[next_dot].pos))
        next_dot += 1
        if next_dot == number_of_dots:
            next_level()
    else:
        lines = []
        next_dot = 0
        dots = []
        create_dots()


def next_level():
    global number_of_dots, lines, dots, next_dot
    number_of_dots += 1
    lines = []
    dots = []
    next_dot = 0
    create_dots()


create_dots()

pgzrun.go()
