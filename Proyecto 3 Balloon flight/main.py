from pgzero.actor import Actor
from random import randint
import pgzrun

# Pantalla
WIDTH = 800  # Ancho
HEIGHT = 600  # Alto

# Actores
balloon = Actor("balloon")
balloon.pos = 400, 300

bird = Actor("bird-up")
bird.pos = randint(800, 1600), randint(10, 200)

house = Actor("house")
house.pos = randint(800, 1600), 460

tree = Actor("tree")
tree.pos = randint(800, 1600), 450

# Variables de juego
bird_up = True
up = False
game_over = False
score = 0
number_of_updates = 0

scores = []


def update_high_scores():
    global score, scores
    filename = "Proyecto 3 Balloon flight/high-scores.txt"
    scores = []
    with open(filename, "r") as file:
        line = file.readline()  # Lee la línea del archivo de puntajes
        high_scores = line.split()
        for high_score in high_scores:
            if score > int(high_score):
                scores.append(f"{score} ")  # Agrego el puntaje que rompe el record
                score = int(high_score)
            else:
                scores.append(f"{high_score} ")  # Agrego el puntaje que ya existía

    with open(filename, "w") as file:
        for high_score in scores:
            file.write(high_score)


def display_high_scores():
    screen.draw.text("HIGH SCORES", (350, 150), color="black")
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(f"{position}. {high_score} puntos", (350, y), color="black")
        position += 1
        y += 25


def draw():
    screen.blit("background", (0, 0))
    if not game_over:
        balloon.draw()
        bird.draw()
        house.draw()
        tree.draw()
        screen.draw.text(f"Score: {score}", (700, 5), color="black")
    else:
        display_high_scores()


def on_mouse_down():
    global up
    up = True
    balloon.y -= 50


def on_mouse_up():
    global up
    up = False


# Aleteo del pajaro
def flap():
    global bird_up
    if bird_up:
        bird.image = "bird-down"
        bird_up = False
    else:
        bird.image = "bird-up"
        bird_up = True


def update():
    global game_over, score, number_of_updates

    if not game_over:
        if not up:
            balloon.y += 1

        # Movimiento de los obstaculos
        # Para el pajaro
        if bird.x > 0:
            bird.x -= 4
            if bird.x <= 400 and bird.x > 396:
                score += 1
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            number_of_updates = 0

        # Para la casa
        if house.right > 0:
            house.x -= 2
            if house.right <= 400 and house.right > 398:
                score += 1
        else:
            house.x = randint(800, 1600)

        # Para el arbol
        if tree.right > 0:
            tree.x -= 2
            if tree.right <= 400 and tree.right > 398:
                score += 1
        else:
            tree.x = randint(800, 1600)

        # Condiciones para perder la partida
        if balloon.top < 0 or balloon.bottom > 560:
            game_over = True
            update_high_scores()

        # Colisión con obstaculos
        if (
            balloon.collidepoint(bird.x, bird.y)
            or balloon.collidepoint(house.x, house.y)
            or balloon.collidepoint(tree.x, tree.y)
        ):
            game_over = True
            update_high_scores()


pgzrun.go()  # Va al final
