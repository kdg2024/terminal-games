#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jul, 06, 2022 15:56:04 by Hiroto Akira

import os
import sys
from operator import attrgetter
from .general import ValueRangeError

class Money:
  def __init__(self,initial_tip,name='あなた',debt=False,play=True):
    if initial_tip<=0:
      raise ValueRangeError("'initial_tip' must be greater than 0.")
    self.initial_tip = initial_tip
    self.own_tip = initial_tip
    self.bet_tip = None
    self.game_counter = 0
    self.miss_counter = 0
    self.hit_counter = 0
    self.name = name
    self.debt = debt
    self.play = play
  def bet(self,tip):
    if not self.debt and not 0 < tip <= self.own_tip:
      raise ValueRangeError("'tip' must be greater than 0 and less than or equal 'self.tip'.")
    else:
      self.own_tip -= tip
      if self.bet_tip==None:
        self.bet_tip = tip
      else:
        self.bet_tip += tip
  def dividend(self,ratio=0,counter_add=True):
    if self.bet == None:
      raise TypeError("'self.bet' must be numerical value")
    else:
      self.own_tip += self.bet_tip*ratio
      self.bet_tip = None
      if counter_add:  # ゲーム中にそのゲーム数を表示するときなど
        self.game_counter += 1
        if ratio==0:
          self.miss_counter += 1
        else:
          self.hit_counter += 1

class Moneys(list):
  def get_play_moneys(self):
    return Moneys([money for money in self if money.play])
  def notip_end(self):
    name_list = []
    for money in self:
      if money.play and money.own_tip <= 0:
        money.play = False
        name_list.append(money.name)
    return name_list
  def get_play_num(self):
    return sum(money.play for money in self)
  def sort_moneys(self,reverse=False):
    self.sort(key=attrgetter('game_counter'),reverse=not reverse)
    self.sort(key=attrgetter('own_tip'),reverse=not reverse)

class Baccarat_Moneys(Moneys):
  def get_play_moneys(self):
    return Baccarat_Moneys([money for money in self if money.play])
  def view(self,clear=True):
    if clear:
      os.system('clear')
    print('='*line_length)
    for money in self:
      delta = money.own_tip-money.initial_tip
      print('【{}の結果】'.format(money.name))
      print('ゲーム数: {}'.format(str(money.game_counter)))
      print('的中    : {}'.format(str(money.hit_counter)))
      print('外れ    : {}'.format(str(money.miss_counter)))
      print('  最終チップ: {}'.format(str(money.own_tip)))
      print('- 初期チップ: {}'.format(str(money.initial_tip)))
      print('-'*(14+max(len(str(money.own_tip)),len(str(money.initial_tip)),len(str(abs(delta)))+1)))
      if delta > 0:
        sign = '+'
      elif delta<0:
        sign = '-'
      else:
        sign = '±'
      print('  収支　　　: {}'.format(sign+str(abs(delta))))
      print('='*line_length)
  def result(self,result_key):
    for i,money in enumerate(self):
      money.result(result_key)
