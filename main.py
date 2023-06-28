import pygame
from pygame.locals import *
import sys
import random

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Colores RGB
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Inicialización de Pygame
pygame.init()
pygame.font.init()  # Inicialización de fuentes

# Creación de la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego KODLAND")


# Clase Jugador
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


# Clase Enemigo
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed_x *= -1
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speed_y *= -1


# Función para iniciar el juego
def iniciar_juego():
    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Creación del jugador
    player = Player()
    all_sprites.add(player)

    # Creación de enemigos
    for _ in range(10):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Tiempo inicial del juego
    start_time = pygame.time.get_ticks()

    # Bucle principal del juego
    running = True
    clock = pygame.time.Clock()
    while running:
        # Limitación de velocidad del bucle principal
        clock.tick(60)

        # Procesamiento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualización de sprites
        all_sprites.update()

        # Detección de colisiones
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            running = False
            end_time = pygame.time.get_ticks()
            duration = (end_time - start_time) / 1000  # Duración en segundos
            mostrar_tiempo(duration)  # Mostrar tiempo de juego
            break

        # Renderizado
        window.fill(WHITE)
        all_sprites.draw(window)
        pygame.display.flip()

    mostrar_menu()  # Vuelve al bucle del menú
    # Cierre de Pygame
    pygame.quit()


# Función para mostrar el tiempo de juego
def mostrar_tiempo(duration):
    # Creación de la ventana del tiempo
    ventana = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tiempo de Juego")

    # Mostrar el tiempo en pantalla
    font = pygame.font.Font(None, 36)
    texto = font.render("Tiempo de juego: " + str(duration) + " segundos",
                        True, GREEN)
    ventana.blit(texto, (WIDTH // 2 - texto.get_width() // 2,
                         HEIGHT // 2 - texto.get_height() // 2))
    pygame.display.flip()

    # Esperar unos segundos antes de volver al menú
    pygame.time.wait(2500)


# Función para mostrar el menú
def mostrar_menu():
    # Creación de la ventana del menú
    ventana = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menú")

    # Cargar el fondo del menú
    fondo = pygame.image.load("5fd1466c9bad3.jpeg").convert()

    # Crear los botones del menú
    boton_jugar = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 50, 200, 50)
    boton_salir = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    iniciar_juego()  # Llama a la función del juego
                    break  # Rompe el bucle del menú
                elif boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Dibujar el fondo del menú
        ventana.blit(fondo, (0, 0))

        # Dibujar los botones
        pygame.draw.rect(ventana, GREEN, boton_jugar)
        pygame.draw.rect(ventana, GREEN, boton_salir)

        # Dibujar el texto de los botones
        font = pygame.font.Font(None, 36)
        texto_jugar = font.render("Jugar", True, WHITE)
        texto_salir = font.render("Salir", True, WHITE)
        ventana.blit(
            texto_jugar,
            (WIDTH / 2 - texto_jugar.get_width() / 2, HEIGHT / 2 - 35))
        ventana.blit(
            texto_salir,
            (WIDTH / 2 - texto_salir.get_width() / 2, HEIGHT / 2 + 65))

        pygame.display.update()


# Llamada inicial al menú
mostrar_menu()
