import pgzrun
import random
from pgzero.actor import Actor

# Color del mensaje al final del juego
FONT_COLOUR = (255, 255, 255)
# Tamaño de la ventana de juego
WIDTH = 800
HEIGHT = 600
# Centro de la pantalla
CENTRE_X = WIDTH / 2
CENTRE_Y = HEIGHT / 2
CENTRE = (CENTRE_X, CENTRE_Y)
# Número de niveles
FINAL_LEVEL = 6
# Velocidad inicial de las estrellas
START_SPEED = 10
# Color de las estrellas que no se deben tocar ❌
COLOURS = ["green", "blue"]

# Variables para terminar el juego
game_over = False
game_complete = False
# Nivel actual
current_level = 1
# Estrellas en la pantalla
stars = []
animations = []


def draw():
    global stars, current_level, game_over, game_complete
    screen.clear()
    screen.blit("space", (0, 0))
    if game_over:
        display_message("GAME OVER!", "Try Again.")
    elif game_complete:
        display_message("YOU WON!", "Well Done.")
    else:
        for star in stars:
            star.draw()


def update():
    global stars
    if len(stars) == 0:
        stars = make_stars(current_level)


def make_stars(number_of_extra_stars):
    colours_to_create = get_colours_to_create(number_of_extra_stars)
    new_stars = create_stars(colours_to_create)
    layout_stars(new_stars)
    animate_stars(new_stars)
    return new_stars


def get_colours_to_create(number_of_extra_stars):
    colours_to_create = ["red"]
    for i in range(0, number_of_extra_stars):
        random_colour = random.choice(COLOURS)
        colours_to_create.append(random_colour)
    return colours_to_create


def create_stars(colours_to_create):
    new_stars = []
    for colour in colours_to_create:
        star = Actor(f"{colour}-star")
        new_stars.append(star)
    return new_stars


# Poner las estrellas en su posición
def layout_stars(stars_to_layout):
    number_of_gaps = len(stars_to_layout) + 1
    gap_size = WIDTH / number_of_gaps
    random.shuffle(stars_to_layout)
    for index, star in enumerate(stars_to_layout):
        new_x_pos = (index + 1) * gap_size
        star.x = new_x_pos


def animate_stars(stars_to_animate):
    for star in stars_to_animate:
        duration = START_SPEED - current_level
        star.anchor = ("center", "bottom")
        animation = animate(
            star, duration=duration, on_finished=handle_game_over, y=HEIGHT
        )
        animations.append(animation)


def handle_game_over():
    global game_over
    game_over = True


def on_mouse_down(pos):
    global stars, current_level
    for star in stars:
        if star.collidepoint(pos):
            if "red" in star.image:
                red_star_click()
            else:
                handle_game_over()


def red_star_click():
    global current_level, stars, animations, game_complete
    stop_animations(animations)  # Detiene las animaciones
    if current_level == FINAL_LEVEL:
        game_complete = True
    else:
        current_level = current_level + 1
        stars = []
        animations = []


def stop_animations(animations_to_stop):
    for animation in animations_to_stop:
        if animation.running:
            animation.stop()


pgzrun.go()
