import pygame
import sys
import random
import os
from gtts import gTTS
from playsound import playsound

# Inicializar Pygame y el módulo de sonido
pygame.init()

# Configuración de la pantalla
width, height = 800, 480  # Mantener 800x480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Batalla de Abecedario - Nivel 2')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BRIGHT_YELLOW = (255, 255, 0)  # Nuevo color más brillante para las barras de vida
LIGHT_BLUE = (0, 176, 240)
GRAY = (169, 169, 169)
DARK_GRAY = (50, 50, 50)
BUTTON_COLOR = (100, 100, 250)
BUTTON_HOVER_COLOR = (150, 150, 250)

# Fuentes
font = pygame.font.Font(None, 40)  # Aumentar la fuente de la pregunta
option_font = pygame.font.Font(None, 54)  # Aumentar la fuente de las opciones

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
    background = pygame.image.load('imagenes/fondonivel2.png')
    background = pygame.transform.scale(background, (width, height - 220))  # Reducimos un poco más el fondo para más espacio

    # Aumentar el tamaño de los personajes
    player_image = pygame.image.load('imagenes/player_sprite.png')
    player_image = pygame.transform.scale(player_image, (120, 120))  # Tamaño aumentado para los personajes

    enemy_image = pygame.image.load('imagenes/enemigonivel2.png')
    enemy_image = pygame.transform.scale(enemy_image, (150, 150))  # Tamaño aumentado para el enemigo

except pygame.error as e:
    print(f"Error al cargar la imagen: {e}")
    pygame.quit()
    sys.exit()

# Ajustar las posiciones de los personajes
player_pos = (250, 74)  # Subir el jugador un poco más
enemy_pos = (600, 25)   # Subir el enemigo otro poco más

# Vida de los personajes
player_health = 100
enemy_health = 100

# Diccionario de preguntas con imágenes (Nivel 2)
questions_images = {
    "A": "imagenes/avion.png",
    "B": "imagenes/burro.png",      
    "C": "imagenes/camisa.png",     
    "D": "imagenes/dedo.png",       
    "E": "imagenes/estrella.png",   
    "F": "imagenes/foco.png",       
    "G": "imagenes/gato.png",       
    "H": "imagenes/helado.png",     
    "I": "imagenes/iglesia.png",    
    "J": "imagenes/jirafa.png",     
    "L": "imagenes/leon.png",       
    "M": "imagenes/manzana.png",    
    "N": "imagenes/nube.png",       
    "O": "imagenes/oso.png",        
    "P": "imagenes/perro.png",      
    "Q": "imagenes/queso.png",      
    "R": "imagenes/raton.png",      
    "S": "imagenes/sol.png",        
    "T": "imagenes/tigre.png",      
    "U": "imagenes/uva.png",        
    "V": "imagenes/vaca.png",       
    "W": "imagenes/wafle.png",      
    "Y": "imagenes/yuca.png",       
    "Z": "imagenes/zorro.png"       
}

# Función para dibujar la barra de vida con borde y color brillante
def draw_health_bar(health, position):
    max_health = 100
    bar_length = 100  # Ajustado para 800x480
    bar_height = 12   # Ajustado para 800x480
    fill = (health / max_health) * bar_length
    pygame.draw.rect(screen, BLACK, (*position, bar_length, bar_height))  # Borde negro
    pygame.draw.rect(screen, BRIGHT_YELLOW, (position[0] + 2, position[1] + 2, fill - 4, bar_height - 4))  # Barra de vida más visible

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

# Función para mostrar la imagen de la pregunta
def draw_screen_with_image(correct_letter, options):
    screen.blit(background, (0, 0))  # Fondo ajustado
    screen.blit(player_image, player_pos)
    screen.blit(enemy_image, enemy_pos)
    draw_health_bar(player_health, (player_pos[0], player_pos[1] - 20))
    draw_health_bar(enemy_health, (enemy_pos[0], enemy_pos[1] - 20))
    
    pygame.draw.rect(screen, DARK_GRAY, (0, 240, 800, 240))  # Expandir el área de pregunta y opciones
    draw_text("¿Con qué letra empieza esta figura?", (50, 250), WHITE, font)  # Subir un poco la pregunta

    # Ajuste del tamaño y posición de la imagen de la figura
    question_image_path = questions_images[correct_letter]
    try:
        question_image = pygame.image.load(question_image_path)
        question_image = pygame.transform.scale(question_image, (120, 120))  # Aumentar tamaño de la imagen
        screen.blit(question_image, (570, 235))  # Centrar la figura
    except pygame.error as e:
        print(f"Error al cargar la imagen: {e}")

    # Opciones debajo de la figura, con más separación vertical
    vertical_spacing = 70  # Aumentar separación vertical
    for i in range(2):
        pygame.draw.rect(screen, GRAY, (50, 350 + i * vertical_spacing, 300, 50))  # Separar las opciones verticalmente
        draw_text(options[i], (200, 360 + i * vertical_spacing), BLACK, option_font)
    for i in range(2, 4):
        pygame.draw.rect(screen, GRAY, (450, 350 + (i - 2) * vertical_spacing, 300, 50))  # Separar más las opciones
        draw_text(options[i], (600, 360 + (i - 2) * vertical_spacing), BLACK, option_font)
    pygame.display.flip()

# Función para dictar la pregunta con gTTS usando playsound para imágenes
def speak_image_question():
    try:
        if os.path.exists("question.mp3"):
            os.remove("question.mp3")
        tts = gTTS(text=f"¿Con qué letra empieza esta figura?", lang='es')
        tts.save("question.mp3")
        playsound("question.mp3")
    except Exception as e:
        print(f"Error al reproducir la pregunta: {e}")

# Función para esperar a que el efecto de sonido termine de reproducirse
def wait_for_sound(sound):
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)

# Función para mostrar el mensaje de victoria o derrota con botón
def display_end_message(message):
    screen.fill(WHITE)  # Fondo blanco
    large_font = pygame.font.SysFont("Comic Sans MS", 72)
    small_font = pygame.font.SysFont("Comic Sans MS", 36)
    draw_text(message, (width // 2 - 350, height // 2 - 100), RED, large_font)
    button_rect = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)
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

# Ciclo del nivel 2
def level_2():
    global player_health, enemy_health
    player_health = 100
    enemy_health = 100
    current_letter = random.choice(list(questions_images.keys()))
    options = generate_options(current_letter)
    draw_screen_with_image(current_letter, options)
    pygame.time.wait(500)
    speak_image_question()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i in range(2):
                    if 50 <= mouse_pos[0] <= 350 and 350 + i * 70 <= mouse_pos[1] <= 400 + i * 70:
                        if options[i] == current_letter:
                            enemy_health -= 20
                            wait_for_sound(random.choice(acierto_sounds))
                        else:
                            player_health -= 20
                            wait_for_sound(random.choice(error_sounds))
                        if player_health <= 0 or enemy_health <= 0:
                            running = False
                            break
                        current_letter = random.choice(list(questions_images.keys()))
                        options = generate_options(current_letter)
                        draw_screen_with_image(current_letter, options)
                        speak_image_question()
                for i in range(2, 4):
                    if 450 <= mouse_pos[0] <= 750 and 350 + (i - 2) * 70 <= mouse_pos[1] <= 400 + (i - 2) * 70:
                        if options[i] == current_letter:
                            enemy_health -= 20
                            wait_for_sound(random.choice(acierto_sounds))
                        else:
                            player_health -= 20
                            wait_for_sound(random.choice(error_sounds))
                        if player_health <= 0 or enemy_health <= 0:
                            running = False
                            break
                        current_letter = random.choice(list(questions_images.keys()))
                        options = generate_options(current_letter)
                        draw_screen_with_image(current_letter, options)
                        speak_image_question()
        pygame.display.flip()
    if enemy_health <= 0:
        display_end_message("¡Has ganado el Nivel 2!")
    else:
        display_end_message("¡Has perdido!")

if __name__ == "__main__":
    level_2()
    pygame.quit()
    sys.exit()
