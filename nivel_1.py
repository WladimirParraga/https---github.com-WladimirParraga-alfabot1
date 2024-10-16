import pygame
import sys
import random
import os
from gtts import gTTS
from playsound import playsound

# Inicializar Pygame y el módulo de sonido
pygame.init()

# Configuración de la pantalla
width, height = 800, 480  # Cambiado a 800x480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Batalla de Abecedario - Nivel 1')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 176, 240)
GRAY = (169, 169, 169)
DARK_GRAY = (50, 50, 50)
BUTTON_COLOR = (100, 100, 250)
BUTTON_HOVER_COLOR = (150, 150, 250)

# Fuentes
font = pygame.font.Font(None, 36)  # Tamaño aumentado para adaptarse al espacio
option_font = pygame.font.Font(None, 48)  # Tamaño aumentado para mejor visibilidad

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
    background = pygame.image.load('imagenes/background.png')
    background = pygame.transform.scale(background, (width, height - 150))  # Ajustado para nueva resolución

    player_image = pygame.image.load('imagenes/player_sprite.png')
    player_image = pygame.transform.scale(player_image, (120, 120))  # Reducido para adaptarse a la nueva resolución

    enemy_image = pygame.image.load('imagenes/enemy_sprite.png')
    enemy_image = pygame.transform.scale(enemy_image, (120, 120))  # Reducido para adaptarse a la nueva resolución

    # Voltear la imagen del enemigo para que mire hacia el jugador
    enemy_image = pygame.transform.flip(enemy_image, True, False)  # Voltear horizontalmente

except pygame.error as e:
    print(f"Error al cargar la imagen: {e}")
    pygame.quit()
    sys.exit()

# Ajustar las posiciones de los personajes más arriba para dejar más espacio
player_pos = (150, 150)  # Mover el jugador hacia arriba
enemy_pos = (580, 150)   # Mover el enemigo hacia arriba

# Vida de los personajes
player_health = 100
enemy_health = 100

# Diccionario de preguntas con todas las letras del abecedario (Nivel 1)
questions = {
    "Avión": "A",
    "Ballena": "B",
    "Casa": "C",
    "Delfín": "D",
    "Elefante": "E",
    "Foca": "F",
    "Gato": "G",
    "Helado": "H",
    "Iglesia": "I",
    "Jirafa": "J",
    "Kilo": "K",
    "León": "L",
    "Manzana": "M",
    "Nube": "N",
    "Oso": "O",
    "Perro": "P",
    "Queso": "Q",
    "Ratón": "R",
    "Sol": "S",
    "Tigre": "T",
    "Uva": "U",
    "Vaca": "V",
    "Wafle": "W",
    "Xilófono": "X",
    "Yate": "Y",
    "Zorro": "Z"
}

used_questions = []  # Lista para evitar la repetición de preguntas

# Función para dibujar la barra de vida con borde
def draw_health_bar(health, position):
    max_health = 100
    bar_length = 120  # Ajustado para adaptarse a la nueva resolución
    bar_height = 15   # Ajustado para adaptarse a la nueva resolución
    fill = (health / max_health) * bar_length
    pygame.draw.rect(screen, BLACK, (*position, bar_length, bar_height))  # Borde negro
    pygame.draw.rect(screen, LIGHT_BLUE, (position[0] + 2, position[1] + 2, fill - 4, bar_height - 4))  # Barra de vida con relleno azul claro

# Función para mostrar texto
def draw_text(text, pos, color=BLACK, font=font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Función para generar opciones manuales
def generate_options(correct_answer):
    options = [correct_answer]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while len(options) < 4:
        option = random.choice(letters)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options

# Función para elegir una nueva pregunta que no se haya usado antes
def choose_new_question():
    available_questions = list(set(questions.keys()) - set(used_questions))
    if available_questions:
        new_question = random.choice(available_questions)
        used_questions.append(new_question)
        return new_question
    else:
        return None

# Función para dictar la pregunta con gTTS usando playsound
def speak_question(question):
    try:
        if os.path.exists("question.mp3"):
            os.remove("question.mp3")
        tts = gTTS(text=f"¿Con qué letra empieza {question}?", lang='es')
        tts.save("question.mp3")
        playsound("question.mp3")
    except Exception as e:
        print(f"Error al reproducir la pregunta: {e}")

# Función para esperar a que el efecto de sonido termine de reproducirse
def wait_for_sound(sound):
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)

# Función para dibujar la pantalla completa con todos los elementos
def draw_screen(question, options):
    screen.blit(background, (0, 0))
    screen.blit(player_image, player_pos)
    screen.blit(enemy_image, enemy_pos)
    draw_health_bar(player_health, (player_pos[0], player_pos[1] - 20))  # Ajustado para nueva resolución
    draw_health_bar(enemy_health, (enemy_pos[0], enemy_pos[1] - 20))     # Ajustado para nueva resolución
    pygame.draw.rect(screen, DARK_GRAY, (0, 320, 800, 160))  # Mover el área inferior más abajo
    draw_text(f"¿Con qué letra empieza {question}?", (50, 330), WHITE, font)
    for i in range(2):
        pygame.draw.rect(screen, GRAY, (50, 380 + i * 50, 300, 40))  # Aumentado para ocupar mejor el espacio
        draw_text(options[i], (200, 385 + i * 50), BLACK, option_font)
    for i in range(2, 4):
        pygame.draw.rect(screen, GRAY, (450, 380 + (i - 2) * 50, 300, 40))  # Aumentado para ocupar mejor el espacio
        draw_text(options[i], (600, 385 + (i - 2) * 50), BLACK, option_font)
    pygame.display.flip()

# Función para mostrar el mensaje de victoria o derrota con botón
def display_end_message(message):
    screen.fill(WHITE)  # Fondo blanco
    large_font = pygame.font.SysFont("Comic Sans MS", 60)  # Ajustado para nueva resolución
    small_font = pygame.font.SysFont("Comic Sans MS", 30)  # Ajustado para nueva resolución
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
                    waiting = False  # Salir y regresar al menú de niveles

# Función para dibujar un botón
def draw_button(text, rect, font):
    pygame.draw.rect(screen, BUTTON_COLOR, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Ciclo del nivel 1
def level_1():
    global player_health, enemy_health
    player_health = 100
    enemy_health = 100

    running = True
    while running:
        current_question = choose_new_question()
        if not current_question:
            display_end_message("¡No quedan más preguntas!")
            break
        
        options = generate_options(questions[current_question])
        draw_screen(current_question, options)
        pygame.time.wait(500)
        speak_question(current_question)

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
                            if options[i] == questions[current_question]:
                                enemy_health -= 20
                                wait_for_sound(random.choice(acierto_sounds))
                            else:
                                player_health -= 20
                                wait_for_sound(random.choice(error_sounds))
                            word_responded = True
                            break
                    for i in range(2, 4):
                        if 450 <= mouse_pos[0] <= 750 and 380 + (i - 2) * 50 <= mouse_pos[1] <= 420 + (i - 2) * 50:
                            if options[i] == questions[current_question]:
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
        display_end_message("¡Has ganado el Nivel 1!")
    else:
        display_end_message("¡Has perdido!")

if __name__ == "__main__":
    level_1()
    pygame.quit()
    sys.exit()
