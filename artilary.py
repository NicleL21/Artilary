import random

"""
Tank class to define an object for game playing
"""
class Tank():
  '''
  Initialize the game with its private variable
  '''
  def __init__(self):
    pass

  '''
  Randomly choose a fire distance and return distance
  '''
  def fire(self):
    pass

  '''
  Take vel and force and return distance
  '''
  def fire(self, velocity, force):
    pass

  '''
  Take damage and decrease the tank hp
  '''
  def take_damage(self, damage):
    pass

  '''
  return the tank hp
  '''
  def get_hp(self):
    pass

"""
Game object to keep track of game flow
"""
class Game():
  '''
  Constructor for the game
  '''
  def __init__(self):
    pass

  '''
  Keep tract of turn
  '''
  def take_turn(self):
    pass

  '''
  Human player activty
  '''
  def human_turn(self):
    pass

  '''
  Computer player activity
  '''
  def computer_turn(self):
    pass

  '''
  Compare the return distance within a error range that would hit it or not
  '''
  def check_hit(self):
    pass

  '''
  Check for loosing condtion that player hp = 0, set game_over
  '''
  def check_lose(self):
    pass

  '''
  Check for winning condition that computer hp = 0, set game_over
  '''
  def check_win(self):
    pass