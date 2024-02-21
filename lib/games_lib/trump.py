#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jul, 06, 2022 15:56:04 by Hiroto Akira

import random
import os
import sys
from .general import ValueRangeError

class Deck:
  def __init__(self):
    code_all = list(range(52))
    self.cards = []
    for i in range(52):
      self.cards.append(Card(code_all.pop(random.randint(0,len(code_all)-1))))
    self.num = 52
  def draw(self,i=0):
    self.num -= 1
    return self.cards.pop(i)

class Hand:
  def __init__(self,name=None):
    self.name = name
    self.cards = []
    self.num = 0
  def draw(self,deck,i=0):
    self.latest_card = deck.draw(i)
    self.cards.append(self.latest_card)
    self.num += 1
  def show_all(self):
    return ' '.join([card.show for card in self.cards])

class Card:
  mark_list = ['♠','♣','♥','◆']
  def __init__(self,code):
    if not 0<=code<= 51:
      raise ValueRangeError("'code' must be in the range 0-51")
    self.code = code
    self.num = code%13+1
    self.mark = __class__.mark_list[code//13]
    if self.num == 1:
      self.show = self.mark+'A'
    elif self.num == 11:
      self.show = self.mark+'J'
    elif self.num == 12:
      self.show = self.mark+'Q'
    elif self.num == 13:
      self.show = self.mark+'K'
    else:
      self.show = self.mark+str(self.num)
 
