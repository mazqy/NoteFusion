import pygame
import time
import sys
import customtkinter as ctk

pygame.init()
root = ctk.CTk()

screen = pygame.display.set_mode(
    (1920, 1080), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
)
print(screen)

white = (255, 255, 255)
black = (0, 0, 0)
black2 = (23, 23, 23)
black3 = (33, 33, 33)
blue = (0, 175, 255)
grey = (175, 175, 175)
yellow = (255, 235, 0)
green = (83, 255, 71)
purple = (215, 0, 225)
combo = 0

key1_color = grey
key2_color = grey
key3_color = grey
key4_color = grey

screen_width = 1920
screen_height = 1080
radius = screen_width / (8 * 4)
print(radius)

col1 = [(480 - 120) + 360 - 15, -60, 0]
col2 = [(480) + 360 - 5, -60, 1]
col3 = [(480 + 120) + 360 + 5, -60, 2]
col4 = [(480 + 240 + 360) + 15, -60, 3]
print(col1)
no_note = True

current_time = 0
start_time = 240 / 1000.0

perfect_timer = 0
perfect_note_hit = False

good_timer = 0
good_note_hit = False

bad_timer = 0
bad_note_hit = False


key_num_set = 0

notes = []
seconds = []
circles_on_scene = []
keys = [False, False, False, False]

durations = []


def set_notes():
    with open(f"beatmaps/{beatmap_selected}/notes.txt", "r", encoding="utf-8") as file:
        lineas = file.readlines()
        for linea in lineas:
            note = linea.split()
            seconds.append(float(note[0]))
            notes.append(int(note[1]))
            if len(note) > 2:
                durations.append(float(note[2]))
            else:
                durations.append(0)


def display_keys():

    screen.blit(imagekey1, (col1[0], 1080 - (radius * 4)))
    screen.blit(imagekey2, (col2[0], 1080 - (radius * 4)))
    screen.blit(imagekey3, (col3[0], 1080 - (radius * 4)))
    screen.blit(imagekey4, (col4[0], 1080 - (radius * 4)))


def create_circle():
    global key_num_set
    global no_note

    key_num = notes[key_num_set]

    if key_num == 1:
        col = col1.copy()
        color = white
    elif key_num == 2:
        col = col2.copy()
        color = green
    elif key_num == 3:
        col = col3.copy()
        color = green
    elif key_num == 4:
        col = col4.copy()
        color = white
    else:
        no_note = True

    if not no_note:
        circles_on_scene.append((screen, color, col, radius))

    key_num_set += 1


def perfect_note():
    global perfect_timer
    global perfect_note_hit

    if perfect_note_hit:
        screen.blit(perfect_text, perfect_center)
        perfect_timer += 1
        if perfect_timer >= 5:
            perfect_note_hit = False
            perfect_timer = 0


def good_note():
    global good_timer
    global good_note_hit

    if good_note_hit:
        screen.blit(good_text, good_center)
        good_timer += 1
        if good_timer >= 5:
            good_note_hit = False
            good_timer = 0


def bad_note():
    global bad_timer
    global bad_note_hit

    if bad_note_hit:
        screen.blit(bad_text, bad_center)
        bad_timer += 1
        if bad_timer >= 5:
            bad_note_hit = False
            bad_timer = 0


circle_speed = 3


def update_circles(dt):
    global combo
    global perfect_note_hit
    global good_note_hit
    global bad_note_hit
    global no_note
    global image
    global image_2

    hit_detected = [False] * 4

    if not no_note:
        for circle in circles_on_scene[:]:
            # pygame.draw.circle(circle[0], circle[1], (circle[2][0], circle[2][1]), circle[3])
            if circle[2][0] == col1[0] or circle[2][0] == col2[0]:

                screen.blit(
                    note_col1,
                    (circle[2][0], circle[2][1]),
                )
            else:
                screen.blit(
                    note_col2,
                    (circle[2][0], circle[2][1]),
                )
            circle[2][1] += circle_speed * dt
            if (
                (1080 - (radius * 4) - 50) <= circle[2][1] <= (1080 - (radius * 4) + 50)
                and keys[circle[2][2]]
                and not hit_detected[circle[2][2]]
            ):
                combo += 1
                perfect_note_hit = True
                circles_on_scene.remove(circle)
                hit_detected[circle[2][2]] = True

            elif (
                (1080 - (radius * 4) - 100)
                <= circle[2][1]
                <= (1080 - (radius * 4) + 100)
                and keys[circle[2][2]]
                and not hit_detected[circle[2][2]]
            ):
                combo += 1
                good_note_hit = True
                circles_on_scene.remove(circle)
                hit_detected[circle[2][2]] = True

            elif (
                (1080 - (radius * 4) - 150)
                <= circle[2][1]
                <= (1080 - (radius * 4) + 150)
                and keys[circle[2][2]]
                and not hit_detected[circle[2][2]]
            ):
                combo += 1
                bad_note_hit = True
                circles_on_scene.remove(circle)
                hit_detected[circle[2][2]] = (
                    True  # Marcar que una nota fue golpeada en esta columna
                )

            elif circle[2][1] > 1080 + 60:
                combo = 0
                circles_on_scene.remove(circle)

    else:
        no_note = False


time_for_timing = 0
song_timed = False


def song_timing():
    global time_for_timing
    global song_timed
    global seconds

    if not song_timed:
        if current_time >= (750 / (circle_speed * targetfps)):
            pygame.mixer.music.play()
            song_timed = True


def counter():
    global current_time
    current_time = pygame.time.get_ticks() / 1000.0 - start_time


game_icon = pygame.image.load("data/cuby.png")
original_note_1 = pygame.image.load("data/note.png")
original_note_1 = pygame.transform.scale(original_note_1, (125, 125))
original_key_note = pygame.image.load("data/hover.png")
original_key_note = pygame.transform.scale(original_key_note, (125, 125))
hit_key_tint = pygame.Surface(original_key_note.get_size())
hit_key_tint.fill((125, 125, 125))
pink_tint = pygame.Surface(original_note_1.get_size())
pink_tint.fill((255, 75, 150))
blue_tint = pygame.Surface(original_note_1.get_size())
blue_tint.fill((255, 255, 255))
imagekey1 = original_key_note.copy()
imagekey2 = original_key_note.copy()
imagekey3 = original_key_note.copy()
imagekey4 = original_key_note.copy()

note_col1 = original_note_1.copy()
note_col2 = original_note_1.copy()

note_col1.blit(pink_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
note_col2.blit(blue_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)


pygame.display.set_caption("NoteFusion")

pygame.display.set_icon(game_icon)


# fonts
font1 = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 35)

# text

perfect_text = font2.render("PERFECT", True, yellow)
good_text = font2.render("GOOD", True, green)
bad_text = font2.render("BAD", True, purple)

perfect_center = perfect_text.get_rect(center=(screen_width / 2, screen_height / 2.4))
good_center = good_text.get_rect(center=(screen_width / 2, screen_height / 2.4))
bad_center = bad_text.get_rect(center=(screen_width / 2, screen_height / 2.4))

# sound effects
hitsound = pygame.mixer.Sound("data/drum-hitclap.ogg")

seconds_set = 0

create = 0
clock = pygame.time.Clock()


targetfps = 540
fps = 540


last_time = time.time()
dt = 0

a = False


def game():
    global screen, beatmap_selected, start_time, song_timed, current_time, seconds_set, a, last_time, seconds_set, imagekey1, imagekey2, imagekey3, imagekey4, note_col1, note_col2, keys

    pygame.mixer.init()
    pygame.mixer.music.load(f"beatmaps/{beatmap_selected}/{beatmap_selected}.mp3")
    set_notes()
    start_time = pygame.time.get_ticks() / 1000.0  # Reinicia el tiempo
    current_time = 0  # Reinicia el tiempo actual
    seconds_set = 0  # Reinicia el índice de las notas
    song_timed = False  # Reinicia la sincronización de la canción

    last_time = time.time()  # Reinicia el último tiempo

    running = True
    while running:

        dt = time.time() - last_time
        dt *= 540
        last_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    keys[0] = True

                    hitsound.play()
                    imagekey1.blit(
                        hit_key_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT
                    )
                if event.key == pygame.K_x:
                    keys[1] = True
                    hitsound.play()
                    imagekey2.blit(
                        hit_key_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT
                    )
                if event.key == pygame.K_n:
                    keys[2] = True
                    hitsound.play()
                    imagekey3.blit(
                        hit_key_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT
                    )
                if event.key == pygame.K_m:
                    keys[3] = True
                    hitsound.play()
                    imagekey4.blit(
                        hit_key_tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT
                    )

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    imagekey1 = original_key_note.copy()
                if event.key == pygame.K_x:
                    imagekey2 = original_key_note.copy()
                if event.key == pygame.K_n:
                    imagekey3 = original_key_note.copy()
                if event.key == pygame.K_m:
                    imagekey4 = original_key_note.copy()

        screen.fill(black2)
        pygame.draw.rect(screen, (black3), (480 + 240 - 12, 0, 510, 1080))
        counter()
        song_timing()
        display_keys()

        if seconds_set >= 0 and seconds_set < len(seconds):
            if current_time >= seconds[seconds_set]:
                create_circle()
                seconds_set += 1
                while (
                    seconds_set < len(seconds)
                    and seconds[seconds_set] == seconds[seconds_set - 1]
                ):
                    create_circle()
                    seconds_set += 1
        else:
            running = False

        update_circles(dt)
        combo_text = font1.render(f"{combo}", True, yellow)
        text_rect = combo_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(combo_text, text_rect)

        perfect_note()
        good_note()
        bad_note()
        keys = [False, False, False, False]

        pygame.display.update()
        clock.tick(fps)


pygame.display.set_caption("Menú de Juego")
can_count = False
# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PINK = (255, 75, 150)
# Fuentes
font = pygame.font.Font(None, 74)

# Texto de las opciones del menú
text_play = font.render("PLAY", True, WHITE)
text_options = font.render("OPTIONS", True, WHITE)
text_exit = font.render("EXIT", True, WHITE)

# Obtener rectángulos de los textos
rect_play = text_play.get_rect(
    center=(screen.get_width() / 2, screen.get_height() / 2 - 100)
)
rect_options = text_options.get_rect(
    center=(screen.get_width() / 2, screen.get_height() / 2)
)
rect_exit = text_exit.get_rect(
    center=(screen.get_width() / 2, screen.get_height() / 2 + 100)
)


def set_can_count():
    global can_count
    can_count = True


# Función principal del menú
def menu():
    global text_play, text_options, text_exit, screen  # Declaramos las variables globales

    while True:
        screen.fill(BLACK)
        screen.blit(text_play, rect_play)
        screen.blit(text_options, rect_options)
        screen.blit(text_exit, rect_exit)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_play.collidepoint(event.pos):
                    select()
                elif rect_options.collidepoint(event.pos):
                    print("Opciones seleccionadas")
                elif rect_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        # Cambia el color del texto si el ratón pasa por encima
        if rect_play.collidepoint(pygame.mouse.get_pos()):
            text_play = font.render("PLAY", True, PINK)

        else:
            text_play = font.render("PLAY", True, WHITE)

        if rect_options.collidepoint(pygame.mouse.get_pos()):
            text_options = font.render("OPTIONS", True, PINK)
        else:
            text_options = font.render("OPTIONS", True, WHITE)

        if rect_exit.collidepoint(pygame.mouse.get_pos()):
            text_exit = font.render("EXIT", True, PINK)
        else:
            text_exit = font.render("EXIT", True, WHITE)

        pygame.display.update()


def select():
    global screen
    import os
    import pygame
    import sys

    # Inicializar Pygame
    pygame.init()

    # Configurar pantalla
    WIDTH, HEIGHT = 1920, 1080
    pygame.display.set_caption("Listar Carpetas")

    # Colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 122, 255)
    LIGHT_BLUE = (0, 162, 255)

    # Fuente
    font = pygame.font.Font(None, 50)

    # Velocidad de desplazamiento
    SCROLL_SPEED = 100

    # Definir clase para los botones de las carpetas
    class BotonCarpeta:
        def __init__(self, rect, carpeta):
            self.rect = rect
            self.carpeta = carpeta
            self.hovered = False

        def draw(self, surface, offset_y):
            rect_moved = self.rect.move(0, offset_y)
            color = (255, 75, 150) if self.hovered else black2
            pygame.draw.rect(surface, color, rect_moved, border_radius=35)
            text_surface = font.render(self.carpeta, True, WHITE)
            surface.blit(text_surface, (rect_moved.x + 20, rect_moved.y + 30))

        def is_hovered(self, mouse_pos, offset_y):
            rect_moved = self.rect.move(0, offset_y)
            return rect_moved.collidepoint(mouse_pos)

    # Definir función para crear botones y listar carpetas
    def listar_carpetas(ruta):
        try:
            carpetas = [
                nombre
                for nombre in os.listdir(ruta)
                if os.path.isdir(os.path.join(ruta, nombre))
            ]
            botones = []
            y = 200
            for carpeta in carpetas:
                boton_rect = pygame.Rect(50, y, 1920 - 100, 150)
                botones.append(BotonCarpeta(boton_rect, carpeta))
                y += 180
            return botones
        except Exception as e:
            print(f"Error al intentar listar carpetas: {e}")
            return []

    def dibujar_botones(botones, offset_y):
        mouse_pos = pygame.mouse.get_pos()
        for boton in botones:
            if boton.is_hovered(mouse_pos, offset_y):
                boton.hovered = True
            else:
                boton.hovered = False
            boton.draw(screen, offset_y)

    # Función para manejar eventos de clic en botones
    def manejar_eventos(botones, offset_y):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    for boton in botones:
                        if boton.is_hovered(event.pos, offset_y):
                            abrir_carpeta(boton.carpeta)
                            game()
                elif event.button == 4:  # Rueda del ratón hacia arriba
                    return SCROLL_SPEED
                elif event.button == 5:  # Rueda del ratón hacia abajo
                    return -SCROLL_SPEED
        return 0

    def abrir_carpeta(carpeta):
        global beatmap_selected
        beatmap_selected = carpeta

    # Configurar la ruta y listar carpetas
    ruta_carpeta = "beatmaps"  # Reemplaza con la ruta de tus carpetas
    botones = listar_carpetas(ruta_carpeta)

    # Variables para el desplazamiento
    offset_y = 0
    max_offset = 0
    min_offset = -max(
        0, (len(botones) * 60) - HEIGHT + 50
    )  # Ajustar según el número de botones y su tamaño

    # Bucle principal
    clock = pygame.time.Clock()
    while True:
        scroll_change = manejar_eventos(botones, offset_y)
        offset_y += scroll_change

        screen.fill(black3)
        dibujar_botones(botones, offset_y)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    menu()
