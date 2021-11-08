'''
This module helps to build the difficulty tabs in the game. Also, the size, orientation, position, and colours of the tabs can be changed. Similarly, this is the module from where numbers can be entered into the boxes.
'''
import pygame as pg

class Tab:
  def __init__(self, a, b, width, height, text = None, colour = (73, 73, 73), highlighter = (189, 189, 189), function = None, params = None):
    self.image = pg.Surface((width, height))
    self.rect = self.image.get_rect()
    pg.display.set_caption('Welcome to THE AMAZING SUDOKU!!!')
    image = pg.image.load('THE AMAZING SUDOKU.png')
    pg.display.set_icon(image)
    self.position = (a, b)
    self.rect.topleft = self.position
    self.text = text
    self.colour = colour
    self.highlighter = highlighter
    self.function = function
    self.params = params
    self.highlighted = False
    self.width = width
    self.height = height

  def update(self, mouse):
    if self.rect.collidepoint(mouse):
      self.highlighted = True
    else:
      self.highlighted = False

  # This function adds the colours in the selected box.
  def draw(self, window):
    if self.highlighted == True:
      self.image.fill(self.highlighter)
    else:
      self.image.fill(self.colour)
    
    if self.text:
      self.input_text(self.text)
    window.blit(self.image, self.position)

  #  This function checks which difficulty-level tab is choosen.
  def click(self):
    if self.params:
      self.function(self.params)
    else:
      self.function()

  # This function helps to input a number (1 to 9) in the small box.
  def input_text(self, text):
    font = pg.font.SysFont("calibri", 20)
    text = font.render(text, False, (0,0,0))
    width, height = text.get_size()
    a = (self.width - width) // 2
    b = (self.height - height) // 2
    self.image.blit(text, (a, b))