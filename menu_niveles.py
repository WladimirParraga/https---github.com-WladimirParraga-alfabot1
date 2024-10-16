# menu_niveles.py
import pygame
import sys
import nivel_1  # Importar el archivo del nivel 1
import nivel_2  # Importar el archivo del nivel 2
import nivel_3  # Importar el archivo del nivel 3

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla (ajustadas a 800x480)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 480

# Colores y fuentes
BLUE = (0, 128, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 102, 204)
HOVER_COLOR = (255, 255, 102)
font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)  # Ajuste de tamaño de fuente para la resolución

# Cargar fondo del menú de niveles
fondo_niveles = pygame.image.load("imagenes/fondonivel.jpg")
fondo_niveles = pygame.transform.scale(fondo_niveles, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Crear botones de niveles (ajustados para la nueva resolución)
boton_nivel_1 = pygame.Rect(90, 360, 160, 70)
boton_nivel_2 = pygame.Rect(275, 280, 160, 70)
boton_nivel_3 = pygame.Rect(500, 190, 160, 70)
boton_regresar = pygame.Rect(20, 20, 160, 70)

# Función para dibujar texto centrado con borde
def draw_text_with_border(text, font, text_color, border_color, surface, rect, border_thickness=3):
    """Función para dibujar texto centrado con borde en un rectángulo."""
    x, y = rect.center
    for dx in range(-border_thickness, border_thickness + 1):
        for dy in range(-border_thickness, border_thickness + 1):
            if dx != 0 or dy != 0:
                border_surface = font.render(text, True, border_color)
                border_rect = border_surface.get_rect(center=(x + dx, y + dy))
                surface.blit(border_surface, border_rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Función para mostrar el menú de niveles
def mostrar_menu_niveles(screen):
    """Función para mostrar el menú de niveles."""
    running = True
    while running:
        screen.blit(fondo_niveles, (0, 0))

        # Obtener la posición del ratón
        mouse_pos = pygame.mouse.get_pos()

        # Dibujar los botones con hover effect
        if boton_nivel_1.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, boton_nivel_1, border_radius=30)
        else:
            pygame.draw.rect(screen, BLUE, boton_nivel_1, border_radius=30)

        if boton_nivel_2.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, boton_nivel_2, border_radius=30)
        else:
            pygame.draw.rect(screen, BLUE, boton_nivel_2, border_radius=30)

        if boton_nivel_3.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, boton_nivel_3, border_radius=30)
        else:
            pygame.draw.rect(screen, BLUE, boton_nivel_3, border_radius=30)

        if boton_regresar.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, boton_regresar, border_radius=30)
        else:
            pygame.draw.rect(screen, BLUE, boton_regresar, border_radius=30)

        # Dibujar texto en los botones
        draw_text_with_border("Nivel 1", font, WHITE, BLACK, screen, boton_nivel_1)
        draw_text_with_border("Nivel 2", font, WHITE, BLACK, screen, boton_nivel_2)
        draw_text_with_border("Nivel 3", font, WHITE, BLACK, screen, boton_nivel_3)
        draw_text_with_border("Regresar", font, WHITE, BLACK, screen, boton_regresar)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar colisiones con los botones y ejecutar los niveles
                if boton_nivel_1.collidepoint(event.pos):
                    print("Nivel 1 seleccionado")
                    nivel_1.level_1()  # Llamar a la función del nivel 1 sin pasar screen
                    return  # Volver al menú de niveles después de jugar
                elif boton_nivel_2.collidepoint(event.pos):
                    print("Nivel 2 seleccionado")
                    nivel_2.level_2()  # Llamar a la función del nivel 2 sin pasar screen
                    return  # Volver al menú de niveles después de jugar
                elif boton_nivel_3.collidepoint(event.pos):
                    print("Nivel 3 seleccionado")
                    nivel_3.level_3()  # Llamar a la función del nivel 3 sin pasar screen
                    return  # Volver al menú de niveles después de jugar
                elif boton_regresar.collidepoint(event.pos):
                    print("Regresando al menú principal...")
                    return "BACK"  # Señal para volver al menú principal

    return "QUIT"
