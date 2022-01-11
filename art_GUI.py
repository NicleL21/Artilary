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
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artilary Game")



def main():
  run = True
  FPS = 60

  clock = pygame.time.Clock()

  def draw_win():
    pygame.draw.rect(WINDOW, WHITE, (0, 200, 800, 200))
    pygame.display.update()

  while run:
    clock.tick(FPS)
    draw_win()


    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

  pygame.quit()


main()