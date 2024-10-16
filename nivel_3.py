import pygame
import sys
import random
import os
from gtts import gTTS
from playsound import playsound

# Inicializar Pygame y el módulo de sonido
pygame.init()

# Configuración de la pantalla
width, height = 800, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Batalla de Abecedario - Nivel 3')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 176, 240)
GRAY = (169, 169, 169)
DARK_GRAY = (50, 50, 50)
BUTTON_COLOR = (100, 100, 250)

# Fuentes
font = pygame.font.Font(None, 36)
option_font = pygame.font.Font(None, 48)

# Cargar efectos de sonido para aciertos y errores
acierto_sounds = [
    pygame.mixer.Sound('sonidos/acierto_1.mp3'),
    pygame.mixer.Sound('sonidos/acierto_2.mp3'),
    pygame.mixer.Sound('sonidos/acierto_3.mp3'),
    pygame.mixer.Sound('sonidos/acierto_4.mp3'),
    pygame.mixer.Sound('sonidos/acierto_5.mp3')
]

error_sounds = [
    pygame.mixer.Sound('sonidos/error_1.mp3'),
    pygame.mixer.Sound('sonidos/error_2.mp3'),
    pygame.mixer.Sound('sonidos/error_3.mp3'),
    pygame.mixer.Sound('sonidos/error_4.mp3'),
    pygame.mixer.Sound('sonidos/error_5.mp3')
]

# Cargar imágenes (Sprites)
try:
    background = pygame.image.load('imagenes/fondonivel3.png')
    background = pygame.transform.scale(background, (width, height - 150))

    player_image = pygame.image.load('imagenes/player_sprite.png')
    player_image = pygame.transform.scale(player_image, (120, 120))

    enemy_image = pygame.image.load('imagenes/enemigonivel3.png')
    enemy_image = pygame.transform.scale(enemy_image, (220, 220))
    enemy_image = pygame.transform.flip(enemy_image, True, False)

except pygame.error as e:
    print(f"Error al cargar la imagen: {e}")
    pygame.quit()
    sys.exit()

# Ajustar las posiciones de los personajes
player_pos = (150, 200)
enemy_pos = (500, 100)

# Vida de los personajes
player_health = 100
enemy_health = 100

# Lista de palabras con letras faltantes
incomplete_words = {
    "Av_on": "I",
    "B_llena": "A",
    "C_sa": "A",
    "Per_o": "R",
    "G_to": "A",
    "R_tón": "A",
    "Hel_do": "A",
    "Sol_dad": "E",
    "C_rro": "A",
    "F_ca": "O",
    "Q_eso": "U",
    "Fr_ta": "U",
    "Maest_a": "R",
    "Cam_o": "P",
    "T_gre": "I",
    "Z_rro": "O",
    "P_to": "A",
    "Ele_ante": "F",
    "M_rrón": "A",
    "Rapi_o": "D",
    "Pl_nta": "A",
    "Bot_lla": "E",
    "Ta_a": "Z",
    "V_ca": "A",
    "Camió_": "N",
    "E_celente": "X",
    "C_mputadora": "O",
    "M_seo": "U",
    "Escrit_rio": "O",
    "G_rra": "O"
}

used_words = []  # Lista para evitar la repetición de palabras

# Función para dibujar la barra de vida con borde
def draw_health_bar(health, position):
    max_health = 100
    bar_length = 120
    bar_height = 15
    fill = (health / max_health) * bar_length
    pygame.draw.rect(screen, BLACK, (*position, bar_length, bar_height))
    pygame.draw.rect(screen, LIGHT_BLUE, (position[0] + 2, position[1] + 2, fill - 4, bar_height - 4))

# Función para mostrar texto
def draw_text(text, pos, color=BLACK, font=font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Función para generar opciones
def generate_options(correct_letter):
    options = [correct_letter]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while len(options) < 4:
        option = random.choice(letters)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options

# Función para elegir una palabra que no se haya usado antes
def choose_new_word():
    available_words = list(set(incomplete_words.keys()) - set(used_words))
    if available_words:
        new_word = random.choice(available_words)
        used_words.append(new_word)
        return new_word
    else:
        return None

# Función para mostrar la palabra incompleta y opciones
def draw_screen_with_incomplete_word(word, options):
    screen.blit(background, (0, 0))
    screen.blit(player_image, player_pos)
    screen.blit(enemy_image, enemy_pos)
    draw_health_bar(player_health, (player_pos[0], player_pos[1] - 20))
    draw_health_bar(enemy_health, (enemy_pos[0], enemy_pos[1] - 20))

    pygame.draw.rect(screen, DARK_GRAY, (0, 320, 800, 160))  
    draw_text(f"Completa la palabra: {word}", (50, 330), WHITE, font)

    # Ajuste para que las opciones estén más espaciadas verticalmente
    for i in range(2):
        pygame.draw.rect(screen, GRAY, (50, 380 + i * 50, 300, 40))
        draw_text(options[i], (200, 385 + i * 50), BLACK, option_font)
    for i in range(2, 4):
        pygame.draw.rect(screen, GRAY, (450, 380 + (i - 2) * 50, 300, 40))
        draw_text(options[i], (600, 385 + (i - 2) * 50), BLACK, option_font)
    pygame.display.flip()

# Función para dictar la instrucción
def speak_incomplete_word():
    try:
        if os.path.exists("question.mp3"):
            os.remove("question.mp3")
        tts = gTTS(text="Completa la palabra con la letra correcta", lang='es')
        tts.save("question.mp3")
        playsound("question.mp3")
    except Exception as e:
        print(f"Error al reproducir la instrucción: {e}")

# Función para esperar a que el efecto de sonido termine de reproducirse
def wait_for_sound(sound):
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)

# Función para mostrar el mensaje de victoria o derrota con botón
def display_end_message(message):
    screen.fill(WHITE)
    large_font = pygame.font.SysFont("Comic Sans MS", 72)
    small_font = pygame.font.SysFont("Comic Sans MS", 36)
    draw_text(message, (width // 2 - 300, height // 2 - 80), RED, large_font)
    button_rect = pygame.Rect(width // 2 - 100, height // 2 + 30, 200, 50)
    draw_button("Regresar", button_rect, small_font)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# Función para dibujar un botón
def draw_button(text, rect, font):
    pygame.draw.rect(screen, BUTTON_COLOR, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Ciclo del nivel 3
def level_3():
    global player_health, enemy_health
    player_health = 100
    enemy_health = 100

    running = True
    while running:
        current_word = choose_new_word()
        if not current_word:
            display_end_message("¡No quedan más palabras!")
            break

        correct_letter = incomplete_words[current_word]
        options = generate_options(correct_letter)

        draw_screen_with_incomplete_word(current_word, options)
        pygame.time.wait(500)
        speak_incomplete_word()

        word_responded = False

        while not word_responded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    word_responded = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i in range(2):
                        if 50 <= mouse_pos[0] <= 350 and 380 + i * 50 <= mouse_pos[1] <= 420 + i * 50:
                            if options[i] == correct_letter:
                                enemy_health -= 20
                                wait_for_sound(random.choice(acierto_sounds))
                            else:
                                player_health -= 20
                                wait_for_sound(random.choice(error_sounds))
                            word_responded = True
                            break
                    for i in range(2, 4):
                        if 450 <= mouse_pos[0] <= 750 and 380 + (i - 2) * 50 <= mouse_pos[1] <= 420 + (i - 2) * 50:
                            if options[i] == correct_letter:
                                enemy_health -= 20
                                wait_for_sound(random.choice(acierto_sounds))
                            else:
                                player_health -= 20
                                wait_for_sound(random.choice(error_sounds))
                            word_responded = True
                            break

            if player_health <= 0 or enemy_health <= 0:
                running = False
                word_responded = True

            pygame.display.flip()

    if enemy_health <= 0:
        display_end_message("¡Has ganado el Nivel 3!")
    elif player_health <= 0:
        display_end_message("¡Has perdido!")
    else:
        display_end_message("¡Juego Terminado!")

if __name__ == "__main__":
    level_3()
    pygame.quit()
    sys.exit()
