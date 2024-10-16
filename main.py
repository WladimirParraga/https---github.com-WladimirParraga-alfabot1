import pygame
import sys
import os
import subprocess
import threading
import webbrowser
import menu_niveles  # Asegúrate de tener importado el archivo para los niveles
from acerca_de import mostrar_acerca_de  # Importamos la función para mostrar la sección "Acerca de"

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla (ajustadas a 800x480)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Aprendizaje del Alfabeto")

# Cargar imágenes para el menú principal
fondo = pygame.image.load("imagenes/image.png")
fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))
joystick_icon = pygame.image.load("imagenes/joystick.png")
interaccion_icon = pygame.image.load("imagenes/interaccion.png")
informacion_icon = pygame.image.load("imagenes/informacion.png")

# Redimensionar imágenes de los botones
icon_size = (120, 120)  # Ajustamos el tamaño para mejor encaje en la nueva resolución
joystick_icon = pygame.transform.scale(joystick_icon, icon_size)
interaccion_icon = pygame.transform.scale(interaccion_icon, icon_size)
informacion_icon = pygame.transform.scale(informacion_icon, icon_size)

# Posiciones de los botones en el menú principal (ajustadas para la nueva resolución y más arriba)
separacion_horizontal = 100
boton_juegos_rect = pygame.Rect(SCREEN_WIDTH // 4 - icon_size[0] // 2 - separacion_horizontal, SCREEN_HEIGHT // 2 - 150, *icon_size)
boton_interaccion_rect = pygame.Rect(SCREEN_WIDTH // 2 - icon_size[0] // 2, SCREEN_HEIGHT // 2 - 150, *icon_size)
boton_informacion_rect = pygame.Rect(SCREEN_WIDTH * 3 // 4 - icon_size[0] // 2 + separacion_horizontal, SCREEN_HEIGHT // 2 - 150, *icon_size)

# Fuentes y colores
font = pygame.font.SysFont("Comic Sans MS", 28, bold=True)  # Ajustamos la fuente a un tamaño menor
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

def draw_text_with_border(text, font, text_color, border_color, surface, x, y, border_thickness=2):
    """Función para dibujar texto con borde."""
    for dx in range(-border_thickness, border_thickness + 1):
        for dy in range(-border_thickness, border_thickness + 1):
            if dx != 0 or dy != 0:
                border_surface = font.render(text, True, border_color)
                border_rect = border_surface.get_rect(center=(x + dx, y + dy))
                surface.blit(border_surface, border_rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def run_flask_app():
    """Función para ejecutar la app Flask en un hilo separado."""
    subprocess.Popen(["python", "app.py"])

# Bucle principal del menú principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Funcionalidad de los botones
            if boton_juegos_rect.collidepoint(event.pos):
                print("Botón Juegos presionado")
                resultado = menu_niveles.mostrar_menu_niveles(screen)  # Abre el menú de niveles como antes
                if resultado == "BACK":
                    continue  # Volver al bucle principal del menú
                elif resultado == "QUIT":
                    running = False
            elif boton_interaccion_rect.collidepoint(event.pos):
                print("Botón Interacción presionado")
                # Ejecutar la aplicación Flask en un hilo separado
                threading.Thread(target=run_flask_app).start()
                webbrowser.open("http://127.0.0.1:5000")  # Abrir la página web del asistente
            elif boton_informacion_rect.collidepoint(event.pos):
                print("Botón Acerca de presionado")
                mostrar_acerca_de(screen)  # Llamamos a la función del archivo acerca_de.py para mostrar la pantalla de "Acerca de"

    # Dibujar el menú principal
    screen.blit(fondo, (0, 0))
    screen.blit(joystick_icon, boton_juegos_rect.topleft)
    screen.blit(interaccion_icon, boton_interaccion_rect.topleft)
    screen.blit(informacion_icon, boton_informacion_rect.topleft)
    draw_text_with_border("Juegos", font, BLUE, WHITE, screen, boton_juegos_rect.centerx, boton_juegos_rect.bottom + 10)
    draw_text_with_border("Interacción", font, BLUE, WHITE, screen, boton_interaccion_rect.centerx, boton_interaccion_rect.bottom + 10)
    draw_text_with_border("Acerca de", font, BLUE, WHITE, screen, boton_informacion_rect.centerx, boton_informacion_rect.bottom + 10)

    pygame.display.update()
