from pgzero.actor import Actor
from random import randint
import pgzrun

# Variables Constantes
WIDTH = 800
HEIGHT = 600
CENTRE_X = WIDTH / 2
CENTRE_Y = HEIGHT / 2

# Variables del juego
move_list = []
display_list = []

score = 0
current_move = 0
count = 4
dance_length = 4

say_dance = False
show_countdown = True
moves_complete = False
game_over = False

# Actores
dancer = Actor("dancer-start")
dancer.pos = CENTRE_X + 5, CENTRE_Y - 40

up = Actor("up")
up.pos = CENTRE_X, CENTRE_Y + 110

right = Actor("right")
right.pos = CENTRE_X + 60, CENTRE_Y + 170

down = Actor("down")
down.pos = CENTRE_X, CENTRE_Y + 230

left = Actor("left")
left.pos = CENTRE_X - 60, CENTRE_Y + 170


def draw():
    global game_over, score, say_dance
    global count, show_countdown

    if not game_over:
        screen.clear()
        screen.blit("stage", (0, 0))
        dancer.draw()
        up.draw()
        down.draw()
        left.draw()
        right.draw()
        screen.draw.text(f"Score: {score}", color="black", topleft=(10, 10))

        if say_dance:
            screen.draw.text(
                "Dance!", color="black", topleft=(CENTRE_X - 65, 150), fontsize=60
            )
        if show_countdown:
            screen.draw.text(
                f"{count}", color="black", topleft=(CENTRE_X - 8, 150), fontsize=60
            )
    else:
        screen.clear()
        screen.blit("stage", (0, 0))
        screen.draw.text(f"Score: {score}", color="black", topleft=(10, 10))
        screen.draw.text(
            "GAME OVER!", color="black", topleft=(CENTRE_X - 130, 220), fontsize=60
        )


def reset_dancer():
    global game_over
    if not game_over:
        dancer.image = "dancer-start"
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"


def update_dancer(move):
    global game_over
    if not game_over:
        if move == 0:  # Flecha arriba
            up.image = "up-lit"
            dancer.image = "dancer-up"
            clock.schedule(reset_dancer, 0.5)
        elif move == 1:  # Flecha derecha
            right.image = "right-lit"
            dancer.image = "dancer-right"
            clock.schedule(reset_dancer, 0.5)
        elif move == 2:  # Flecha abajo
            down.image = "down-lit"
            dancer.image = "dancer-down"
            clock.schedule(reset_dancer, 0.5)
        elif move == 3:  # Flecha izquierda
            left.image = "left-lit"
            dancer.image = "dancer-left"
            clock.schedule(reset_dancer, 0.5)


def display_moves():
    global move_list, display_list, dance_length
    global say_dance, show_countdown, current_move
    if display_list:
        this_move = display_list[0]  # Primer movimiento
        display_list = display_list[1:]  # Elimino el movimiento de la lista
        if this_move == 0:
            update_dancer(0)
            clock.schedule(display_moves, 1)
        elif this_move == 1:
            update_dancer(1)
            clock.schedule(display_moves, 1)
        elif this_move == 2:
            update_dancer(2)
            clock.schedule(display_moves, 1)
        elif this_move == 3:
            update_dancer(3)
            clock.schedule(display_moves, 1)
    else:
        say_dance = True
        show_countdown = False


def generate_moves():
    global move_list, dance_length, count
    global show_countdown, say_dance

    count = 4
    move_list = []
    say_dance = False
    for move in range(0, dance_length):  # n movimientos aleatorios
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)
    show_countdown = True
    countdown()


def countdown():  # Conteo regresivo
    global count, game_over, show_countdown
    if count > 1:
        count -= 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()


def next_move():
    global dance_length, current_move, moves_complete
    if current_move < dance_length - 1:  # Existen aun movimientos por hacer?
        current_move += 1
    else:
        moves_complete = True


def on_key_up(key):
    global score, game_over, move_list, current_move
    if key == keys.UP:
        update_dancer(0)
        if move_list[current_move] == 0:
            score += 1
            next_move()
        else:
            game_over = True
    elif key == keys.RIGHT:
        update_dancer(1)
        if move_list[current_move] == 1:
            score += 1
            next_move()
        else:
            game_over = True
    elif key == keys.DOWN:
        update_dancer(2)
        if move_list[current_move] == 2:
            score += 1
            next_move()
        else:
            game_over = True
    elif key == keys.LEFT:
        update_dancer(3)
        if move_list[current_move] == 3:
            score += 1
            next_move()
        else:
            game_over = True


generate_moves()
music.play("vanishing-horizon")


def update():
    global game_over, current_move, moves_complete
    if not game_over:
        if moves_complete:
            generate_moves()
            moves_complete = False
            current_move = 0
    else:
        music.stop()


pgzrun.go()  # Ultima linea
