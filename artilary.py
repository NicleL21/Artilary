import random
import unittest
import numpy as np

"""
Tank class to define an object for game playing
"""
class Tank():

  # Initialize the game with hp and set defaults
  def __init__(self, hp=1):
    self.hp = hp

   #Randomly choose a fire distance and return distance
  def fire(self):
    velocity = random.randint(1, 100)
    angle = random.randint(1, 90)
    return self.calculate_distance(velocity, angle)

  # Take vel and angle of the tank from the player and return distance
  def human_fire(self):
    angle = 0
    while angle <= 0 or angle > 90:
      print("Please enter the firing velocity and angle of your tank within(0, 90)")
      velocity, angle = map(int, input().split())
    return self.calculate_distance(velocity, angle)

  # Sub function use to calculate distance of the fire
  def calculate_distance(self, velocity, angle):
    if 1 < angle < 90:
      radian = np.deg2rad(angle)
      distance = (int)((velocity**2 * np.cos(2 * radian)) / (2 * 10))
    else:
      distance = 0
    return distance

  # Take damage and decrease the tank hp
  def take_damage(self, damage):
    # negative damge case
    if damage < 0:
      damage = 0

    self.hp -= damage

    #keep tract of damage
    if self.hp < 0:
      self.hp = 0

  # return the tank hp
  def get_hp(self):
    return self.hp

"""
Game object to keep track of game flow
"""
class Game():
  # Constructor for the game
  def __init__(self):
    self.result = False
    self.game_over = False
    self.distance = random.randint(100, 200)

    self.human = Tank()
    self.computer = Tank()

  # Keep tract of turn
  def take_turn(self):
    turn = 0
    while not self.game_over:
      if turn % 2 == 0:
        self.human_turn()
      else:
        self.computer_turn()
      turn += 1

  # Human player activty
  def human_turn(self):
    fire = self.human.human_fire()
    if self.check_hit(fire):
      print("You hit your enemy!")
      self.computer.take_damage(1)
    else:
      print("You miss them, better try next time!")


  # Computer player activity
  def computer_turn(self):
    fire = self.computer.fire()
    if self.check_hit(fire):
      print("You enemy hit you :(")
      self.human.take_damage(1)
    else:
      print("You enemy miss a shot :)")

  # Compare distance of shot and the return boolean of hit or not within an error range
  def check_hit(self, distance):
    if self.distance - 10 <= distance <= self.distance + 10:
      return True
    return False

  #Check for loosing condtion that player hp = 0, set game_over
  def check_lose(self):
    if self.human.get_hp() == 0:
      self.result = False
      self.game_over = True

  # Check for winning condition that computer hp = 0, set game_over
  def check_win(self):
    if self.computer.get_hp() == 0:
      self.result = True
      self.game_over = True

  # Getter distance for checking
  def get_distance(self):
    return self.distance

  # Getter game_over
  def get_game_over(self):
    return self.result

"""
Test case for class Tank
"""
class Testing(unittest.TestCase):
  # case 1: 1 dmg
  def test_hp1(self):
    tank1 = Tank()
    tank1.take_damage(1)
    self.assertEqual(tank1.get_hp(), 9)

  # case 2: negative dmg
  def test_hp2(self):
    tank = Tank()
    tank.take_damage(-5)
    self.assertEqual(tank.get_hp(), 10)

  # case 3: large dmg
  def test_hp3(self):
    tank = Tank()
    tank.take_damage(50)
    self.assertEqual(tank.get_hp(), 0)

  # case 4: two damage
  def test_hp4(self):
    tank = Tank()
    tank.take_damage(5)
    tank.take_damage(-5)
    self.assertEqual(tank.get_hp(), 5)

  # case 1: test cacluation of fire tank
  def test_calc1(self):
    tank = Tank()
    self.assertEqual(tank.calculate_distance(50, 30), 62)

  # case 2: test angle < 1
  def test_calc2(self):
    tank = Tank()
    self.assertEqual(tank.calculate_distance(50, -4), 0)

  # case 3: test angle > 90
  def test_calc3(self):
    tank = Tank()
    self.assertEqual(tank.calculate_distance(50, 91), 0)

  # case 0: check distance
  def test_game_distance(self):
    game = Game()
    self.assertTrue(100 <= game.get_distance() <= 200)

  # case 1: check function of hit method
  def test_game_check_hit(self):
    game = Game()
    dis = game.get_distance()
    self.assertEqual(game.check_hit(dis), True)

  # case 2: check for upper boundary
  def test_game_check_hit1(self):
    game = Game()
    dis = game.get_distance() - 10
    self.assertEqual(game.check_hit(dis), True)

  # case 3: check for lower boundary
  def test_game_check_hit1(self):
    game = Game()
    dis = game.get_distance() + 10
    self.assertEqual(game.check_hit(dis), True)


if __name__ == '__main__':
    # Calling the unittest case
    # unittest.main()

    score = 0
    total = 0
    keep_playing = True

    print('Welcome to the artilary game! Lets start!')
    while keep_playing:
      print('Press y to strart, n to stop the game')
      ans = input()
      if ans == 'y':

        total += 1

        game = Game()
        game.take_turn()

        if game.get_game_over:
          print("Congratulation! You win the game!")
          score += 1
        else:
          print("Better luck next time!")

      print('Score of game play')
      print('Total win rate: ', int(score / total * 100))




