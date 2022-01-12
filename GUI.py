import pygame
import random
import os
import numpy as np

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (93, 93, 93)

WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artilary Game")

# Load assets
TANK_GREEN = pygame.image.load(os.path.join("assets", "pixel_tank1.jpg"))
TANK_GREEN2 = pygame.transform.scale(TANK_GREEN, (200, 100))
TANK_RED = pygame.image.load(os.path.join("assets", "pixel_tank2.jpg"))
TANK_RED2 = pygame.transform.scale(TANK_RED, (200, 100))
BG = pygame.image.load(os.path.join("assets", "background.png"))
BG2 = pygame.transform.scale(BG, (WIDTH, HEIGHT))

"""
Tank class to define an object for game playing
"""
class Tank():

  # Initialize the game with hp and set defaults
  def __init__(self, x, y, hp=100):
    self.x = x
    self.y = y
    self.hp = hp
    self.img = None

   #Randomly choose a fire distance and return distance
  def fire(self):
    velocity = random.randint(1, 200)
    angle = random.randint(1, 90)
    if 1 < angle < 90:
      radian = np.deg2rad(angle)
      distance = (int)((velocity**2 * np.sin(2 * radian)) / (2 * 10))
    else:
      distance = 0
    return distance

  # Draw tank
  def draw(self, window):
    window.blit(self.img, (self.x, self.y))

  # return the tank hp
  def get_hp(self):
    return self.hp

  def get_width(self):
    return self.img.get_width()

  def get_length(self):
    return self.img.get_height()

'''
Player tank obj
'''
class Player(Tank):
  def __init__(self, x, y, hp=100):
    super().__init__(x, y)
    self.img = TANK_GREEN2

  # Override to modify angle
  def fire(self, angle, velocity):
    if 1 < angle < 90:
      radian = np.deg2rad(angle)
      distance = (int)((velocity**2 * np.sin(2 * radian)) / (2 * 10))
    else:
      distance = 0
    return distance

'''
Enemy tank obj
'''
class Enemy(Tank):
  def __init__(self, x, y, hp=100):
    super().__init__(x, y)
    self.img = TANK_RED2

def main():
  game_font = pygame.font.SysFont("comicsans", 30)
  BOX_LENGHT, BOX_HEIGHT = 40, 20
  X_BOX1 = 180
  X_BOX2 = 240
  Y_BOX1 = 26
  Y_BOX2 = 62

  run = True
  FPS = 60
  clock = pygame.time.Clock()

  angle = 0
  velocity = 0

  player = Player(20, HEIGHT - 140)
  # Update the x of enemy randow later
  enemy = Enemy(600, HEIGHT - 140)

  def redraw_win():

    SCREEN.blit(BG2, (0, 0))

    # Draw text
    angle_label = game_font.render(f"Angle: {angle}", 1, BLACK)
    velocity_label = game_font.render(f"Velocity: {velocity}", 1, BLACK)
    SCREEN.blit(angle_label, (10, 10))
    SCREEN.blit(velocity_label, (10, angle_label.get_height() + 10))

    # Draw button
    pygame.draw.rect(SCREEN, GREY, (X_BOX1, Y_BOX1, BOX_LENGHT, BOX_HEIGHT))
    pygame.draw.rect(SCREEN, GREY, (X_BOX1, Y_BOX2, BOX_LENGHT, BOX_HEIGHT))
    pygame.draw.rect(SCREEN, GREY, (X_BOX2, Y_BOX1, BOX_LENGHT, BOX_HEIGHT))
    pygame.draw.rect(SCREEN, GREY, (X_BOX2, Y_BOX2, BOX_LENGHT, BOX_HEIGHT))

    box_11_label = game_font.render("<", True, WHITE)
    box_12_label = game_font.render("<", True, WHITE)
    box_21_label = game_font.render(">", True, WHITE)
    box_22_label = game_font.render(">", True, WHITE)
    SCREEN.blit(box_11_label, (X_BOX1 + 15, Y_BOX1 - 15))
    SCREEN.blit(box_12_label, (X_BOX1 + 15, Y_BOX2 - 15))
    SCREEN.blit(box_21_label, (X_BOX2 + 15, Y_BOX1 - 15))
    SCREEN.blit(box_22_label, (X_BOX2 + 15, Y_BOX2 - 15))

    player.draw(SCREEN)
    enemy.draw(SCREEN)

    pygame.display.update()

  # Game main
  while run:
    clock.tick(FPS)
    redraw_win()

    # Checking event
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

  pygame.quit()


main()