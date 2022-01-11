import pygame
import random
import os
import time

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artilary Game")

# Load assets
TANK_GREEN = pygame.image.load(os.path.join("assets", "pixel_tank1.png"))
TANK_RED = pygame.image.load(os.path.join("assets", "pixel_tank2.jpg"))
BG = pygame.image.load(os.path.join("assets", "background.png"))
BG2 = pygame.transform.scale(BG, (WIDTH, HEIGHT))


def main():
  game_font = pygame.font.SysFont("comicsans", 30)

  run = True
  FPS = 60
  clock = pygame.time.Clock()

  angle = 0
  velocity = 0

  def redraw_win():

    SCREEN.blit(BG2, (0, 0))

    angle_label = game_font.render(f"Angle: {angle}", 1, BLACK)
    velocity_label = game_font.render(f"Velocity: {velocity}", 1, BLACK)
    SCREEN.blit(angle_label, (10, 10))
    SCREEN.blit(velocity_label, (10, angle_label.get_height() + 10))


    # pygame.draw.rect(SCREEN, WHITE, (0, 200, 800, 200))

    pygame.display.update()

  while run:
    clock.tick(FPS)
    redraw_win()


    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

  pygame.quit()


main()