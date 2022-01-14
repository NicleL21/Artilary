from termios import VEOL
import pygame
import random
import os
import numpy as np
from pygame.constants import MOUSEBUTTONDOWN

pygame.font.init()
game_font = pygame.font.SysFont("comicsans", 30)

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
CANNON = pygame.image.load(os.path.join("assets", "cannon.png"))
CANNON2 = pygame.transform.scale(CANNON, (50, 50))

"""
The cannon ball object that the tank fire
"""
class Cannonball():
  def __init__(self, x, y):
      self.x = x
      self.y = y
      self.img = CANNON2
      self.mask = pygame.mask.from_surface(self.img)

  def draw(self, window):
    window.blit(self.img, (self.x, self.y))

  # Motion of the ball
  def move(self, angle, velocity):
    self.x += 1
    self.y = 210 + self.x * np.tan(angle) - 9.8 * self.x**2 / 2 * velocity**2  * np.cos(angle)**2
    print(self.y)

  # Check the ball if it is off screen
  def off_screen(self, height):
    return not(self.y <= height and self.y >= 0)



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
    self.angle = 0
    self.velocity = 0
    self.cannon = None

   # Create a cannon ball and call it to move
  def fire(self):
    if self.cannon == None:
      self.cannon = Cannonball(self.x + self.get_width(), self.y)
    if 0 <= self.angle <= 90:
      radian = np.deg2rad(self.angle)
      #self.cannon.move(radian, self.velocity)

  # the end turn flag
  def end_turn(self):
    if self.cannon != None and self.cannon.y > HEIGHT - 130:
      return True
    return False

  # Draw tank
  def draw(self, window):
    window.blit(self.img, (self.x, self.y))
    if self.cannon != None:
      self.cannon.draw(window)

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

  def increase_angel(self):
    if self.angle < 90:
      self.angle += 1

  def decrease_angle(self):
    if self.angle > 1:
      self.angle -= 1

  def increase_velocity(self):
    if self.velocity < 200:
      self.velocity += 1

  def decrease_velocity(self):
    if self.velocity > 100:
      self.velocity -= 1

  def get_angle(self):
    return self.angle

  def get_velocity(self):
    return self.velocity

'''
Enemy tank obj
'''
class Enemy(Tank):
  def __init__(self, x, y, hp=100):
    super().__init__(x, y)
    self.img = TANK_RED2

# Check the overlap of the pixels
def collision(obj1, obj2):
  offset_x = obj2.x - obj1.x #(x,y) of top left corner
  offset_y = obj2.y - obj1.y
  # overlap the pixels when use mask
  return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():

  run = True
  FPS = 60
  clock = pygame.time.Clock()

  turn = 0
  distance = random.randint(100, 200)

  player = Player(20, HEIGHT - 140)
  # Update the x of enemy randow later
  enemy = Enemy(20 + player.get_width() + distance, HEIGHT - 140)

  def redraw_win():

    SCREEN.blit(BG2, (0, 0))

    # Draw text
    angle_label = game_font.render(f"Angle: {player.get_angle()}", 1, BLACK)
    velocity_label = game_font.render(f"Velocity: {player.get_velocity()}", 1, BLACK)
    SCREEN.blit(angle_label, (10, 10))
    SCREEN.blit(velocity_label, (10, angle_label.get_height() + 10))

    player.draw(SCREEN)
    enemy.draw(SCREEN)

    pygame.display.update()

  def computer_turn():
    pass

  def check_win():
    pass

  def check_lose():
    pass

  # Game main
  while run:
    clock.tick(FPS)
    redraw_win()

    # Checking event
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    if turn % 2 == 0:
      # Human turn
      keys = pygame.key.get_pressed()
      if keys[pygame.K_UP]:
        player.increase_angel()
      if keys[pygame.K_DOWN]:
        player.decrease_angle()
      if keys[pygame.K_LEFT]:
        player.decrease_velocity()
      if keys[pygame.K_RIGHT]:
        player.increase_velocity()

      if keys[pygame.K_SPACE]:
        player.fire()

      if player.end_turn():
        turn += 1

    else:
      computer_turn()

    check_win()
    check_lose()

  pygame.quit()


main()