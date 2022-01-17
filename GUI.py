from termios import VEOL
import pygame
import random
import os
import numpy as np
from pygame.constants import MOUSEBUTTONDOWN

pygame.font.init()
game_font = pygame.font.SysFont("comicsans", 30)
noti_font = pygame.font.SysFont("comicsans", 50)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (93, 93, 93)

WIDTH, HEIGHT = 1400, 700
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

def delta_y(velocity, angle, shift_origin_x):
  delta_y = (int)(- (shift_origin_x * np.tan(angle) - (9.8 * shift_origin_x**2) / (2 * velocity**2  * np.cos(angle)**2)))
  return delta_y

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


  # Motion of the ball for human
  def move(self, angle, velocity, tank_x, tank_y):
    new_x = self.x + 5

    shift_origin_x = self.x - tank_x
    traject = delta_y(velocity, angle, shift_origin_x)
    new_y = tank_y + traject

    self.x = new_x
    self.y = new_y

  # Motion of the ball for computer
  def cmove(self, angle, velocity, tank_x, tank_y):
    new_x = self.x - 5

    shift_origin_x = self.x - tank_x
    traject = delta_y(velocity, angle, - shift_origin_x)
    new_y = tank_y + traject

    self.x = new_x
    self.y = new_y
    print(new_x, new_y)

  # Check the ball if it is off screen
  def off_screen(self):
    return not(0 <= self.y <= HEIGHT and 0 <= self.x <= WIDTH)

  # to check if the laser collide with obj # Check the overlap of the pixels
  def collision(self, obj):
    offset_x = obj.x - self.x #(x,y) of top left corner
    offset_y = obj.y - self.y
    # overlap the pixels when use mask
    return self.mask.overlap(obj.mask, (offset_x, offset_y)) != None

"""
Tank class to define an object for game playing
"""
class Tank():

  # Initialize the game with hp and set defaults
  def __init__(self, x, y, hp=10):
    self.x = x
    self.y = y
    self.hp = hp
    self.img = None
    self.angle = 0
    self.velocity = 0
    self.cannon = []

  # Draw tank
  def draw(self, window):
    window.blit(self.img, (self.x, self.y))
    for cannon in self.cannon:
      if not (cannon.off_screen()):
        cannon.draw(window)

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
  def __init__(self, x, y, hp=10):
    super().__init__(x, y)
    self.img = TANK_GREEN2
    self.mask = pygame.mask.from_surface(self.img)

  # Create a cannon ball
  def fire(self):
    if 0 < self.angle < 90 and 0 < self.velocity:
      self.cannon.append(Cannonball(self.x + self.get_width(), self.y))

  # Move the cannon
  def move_cannon(self, obj):
    radian = np.deg2rad(self.angle)
    for cannon in self.cannon:
      cannon.move(radian, self.velocity, self.x + self.get_width(), self.y)
      if cannon.off_screen():
        self.cannon.remove(cannon)
      elif cannon.collision(obj):
        obj.hp -= 10


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
    if self.velocity > 1:
      self.velocity -= 1

  def move_left(self):
    if self.x > 0:
      self.x -= 1

  def move_right(self):
    if self.x < WIDTH - self.get_width():
      self.x += 1

  def get_angle(self):
    return self.angle

  def get_velocity(self):
    return self.velocity

'''
Enemy tank obj
'''
class Enemy(Tank):
  def __init__(self, x, y, hp=10):
    super().__init__(x, y)
    self.img = TANK_RED2
    self.mask = pygame.mask.from_surface(self.img)

  # Create a cannon ball
  def fire(self):
    self.angle = random.randint(0, 89)
    self.velocity = random.randint(0, 200)
    if 0 < self.angle < 90 and 0 < self.velocity:
      self.cannon.append(Cannonball(self.x + self.get_width(), self.y))

  # Move the cannon
  def move_cannon(self, obj):
    radian = np.deg2rad(self.angle)
    for cannon in self.cannon:
      cannon.cmove(radian, self.velocity, self.x, self.y)
      if cannon.off_screen():
        self.cannon.remove(cannon)
      elif cannon.collision(obj):
        obj.hp -= 10

def human_turn(player):
  keys = pygame.key.get_pressed()

  if keys[pygame.K_UP]:
    player.increase_angel()
  if keys[pygame.K_DOWN]:
    player.decrease_angle()
  if keys[pygame.K_LEFT]:
    player.decrease_velocity()
  if keys[pygame.K_RIGHT]:
    player.increase_velocity()

  # Call the tank to fire
  if keys[pygame.K_SPACE]:
    player.fire()


def main():
  run = True
  win = False
  win_count = 0
  lost = False
  lose_count =0
  FPS = 60
  clock = pygame.time.Clock()

  turn = 0
  distance = random.randint(200, 700)

  player = Player(20, HEIGHT - 140)
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

    if lost:
      lost_label = noti_font.render("You lost!", 1, WHITE)
      SCREEN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, HEIGHT / 2))

    if win:
      win_label = noti_font.render("Congrats!", 1, WHITE)
      SCREEN.blit(win_label, (WIDTH / 2 - win_label.get_width() / 2, HEIGHT / 2))

    pygame.display.update()

  # the end turn flag
  def end_turn(obj):
    for cannon in obj.cannon:
      if cannon.y > HEIGHT - 130:
        return True
    return False

  # Game main
  while run:
    clock.tick(FPS)
    redraw_win()

    # Win check
    if enemy.hp == 0:
      win = True
      win_count += 1

    if win:
      if win_count > FPS * 3:
        run = False
      else:
        continue

    # Lose check
    if player.hp == 0:
      lost = False
      lose_count += 1

    if lost:
      if lose_count > FPS * 3:
        run = False
      else:
        continue

    # Checking event
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    if turn % 2 == 0:
      # Human turn
      human_turn(player)

      if end_turn(player):
        turn += 1
    else:
      # Enemy turn
      enemy.fire()
      if end_turn(enemy):
        turn += 1

    player.move_cannon(enemy)
    enemy.move_cannon(player)



  pygame.quit()


main()