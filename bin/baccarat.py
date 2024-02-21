#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jul, 06, 2022 15:56:04 by Hiroto Akira

import random
import os
import sys
from operator import attrgetter
from games_lib import ValueRangeError
from games_lib.trump import Card, Deck, Hand
from games_lib.money import Money, Moneys

class Baccarat_Hand(Hand):
  def __init__(self,name=None):
    super().__init__(name)
    self.score = 0
    self.three = None
  def draw(self,deck,i=0):
    super().draw(deck,i)
    card_score = min(self.latest_card.num,10) % 10
    self.score = (self.score + card_score) % 10  # 1の位だけのため
    if self.num == 3:
      self.three = card_score

class Baccarat_Money(Money):
  predict_dic = {1:'プレイヤーの勝利',
2:'バンカーの勝利',
3:'引き分け'}
  choice_text ="""\
1: {}(1.95倍)
2: {}(2倍)
3: {}(9倍)\
""".format(predict_dic[1],predict_dic[2],predict_dic[3])
  def __init__(self,initial_tip,name='あなた'):
    super().__init__(initial_tip,name)
    self.predict_key = None
    self.predict_value = None
  def predict(self,predict_key):
    self.predict_key = predict_key
    self.predict_value = __class__.predict_dic[self.predict_key]
  def result(self,result_key):
    # チップの処理
    hit_text = '{0}の予想は当たりました！\n{0}がベットしていたチップは'.format(self.name)+ '{}倍になって返却されます．'
    if self.predict_key!=result_key:
      print('{0}の予想は外れました...\n{0}がベットしていたチップは没収されます．'.format(self.name))
      self.dividend() 
    elif result_key == 1:
      print(hit_text.format('1.95'))
      self.dividend(ratio=1.95)
    elif result_key == 2:
      print(hit_text.format('2'))
      self.dividend(ratio=2)
    elif result_key == 3:
      print(hit_text.format('9'))
      self.dividend(ratio=9)
    self.predict_key = None
    self.predict_value = None

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

def yn_inf(text,sep=' '):
  while True:
    ans = input(text+sep+'(y/n): ')
    if ans == 'y':
      return True
    elif ans == 'n':
      return False

def clear_print_head(moneys,game_counter_add=True):
  os.system('clear')
  print('='*line_length)
  if game_counter_add:
    game_counter = moneys[0].game_counter + 1
  else:
    game_counter = moneys[0].game_counter
  print('【{}ゲーム目】'.format(str(game_counter)))
  for money in moneys:
    print('[{}] 所持チップ: {} ベット: {} 予想: {}'.format(money.name,money.own_tip,money.bet_tip,money.predict_value))
  print('='*line_length)

def view(deck,player,banker,moneys,game_counter_add=True):
  clear_print_head(moneys,game_counter_add)
  print('山札の残り枚数: {}'.format(str(deck.num)))
  print('{}の手札: {} ({})'.format(player.name,player.show_all(),player.score))
  print('{}の手札: {} ({})'.format(banker.name,banker.show_all(),banker.score))
  print('='*line_length)

def input_draw_view(deck,player,banker,moneys,player_draw=True,check_draw=True):
  # playerがカード引く場合はplayer_draw=True．
  # bankerがカード引く場合はplayer_draw=False．
  if player_draw:
    if check_draw:
      input('{}がカードを引きます．(enter)'.format(player.name))
    player.draw(deck)
    view(deck,player,banker,moneys)
  else:
    if check_draw:
      input('{}がカードを引きます．(enter)'.format(banker.name))
    banker.draw(deck)
    view(deck,player,banker,moneys)

def baccarat(moneys,check_draw=True):
  clear_print_head(moneys)
  # 予想する
  for money in moneys:
    print(Baccarat_Money.choice_text)
    while True:
      try:
        money.predict(int(input('{}の予想: '.format(money.name))))
        break
      except (KeyError,ValueError) :
        print('1,2,3の中から選択して入力してください．')
    clear_print_head(moneys)
    # ベットする
    while True:
      try:
        money.bet(float(input('{}のベット額: '.format(money.name))))
        break
      except ValueError:
        print('数値を入力してください.')
      except ValueRangeError:
        print('0より大きくて所持チップ額({})より小さい数値を入力してください．'.format(str(money.own_tip)))
    clear_print_head(moneys)
  
  # ゲームスタート
  deck = Deck()
  player = Baccarat_Hand('プレイヤー')
  banker = Baccarat_Hand('バンカー')
  view(deck,player,banker,moneys)
  if check_draw:
    input('カードを配ります．(enter)')
  player.draw(deck)
  player.draw(deck)
  banker.draw(deck)
  banker.draw(deck)
  view(deck,player,banker,moneys)

  # ナチュラルとそうでない場合で分ける.
  # ナチュラルの場合
  if player.score >= 8 or banker.score >=8:
    pass
  # ナチュラルでない場合
  else:
    # プレイヤーが二枚目で終了する条件及びその場合
    if player.score>=6:
      # バンカーのターン
      if banker.score<=5:
        input_draw_view(deck,player,banker,moneys,player_draw=False,check_draw=check_draw)
    # プレイヤーが三枚目を引く条件及びその場合
    else:
      input_draw_view(deck,player,banker,moneys,player_draw=True,check_draw=check_draw)
      # バンカーのターン
      if banker.score<=2:
        input_draw_view(deck,player,banker,moneys,player_draw=False,check_draw=check_draw)
      elif banker.score==3 and (0<=player.three<=7 or player.three==9):
        input_draw_view(deck,player,banker,moneys,player_draw=False,check_draw=check_draw)
      elif banker.score==4 and 2<=player.three<=7:
        input_draw_view(deck,player,banker,moneys,player_draw=False,check_draw=check_draw)
      elif banker.score==5 and 4<=player.three<=7:
        input_draw_view(deck,player,banker,moneys,player_draw=False,check_draw=check_draw)
      elif banker.score==6 and 6<=player.three<=7:
        input_draw_view(deck,player,banker,moneys,player_draw=False,check_draw=check_draw)

  # 結果を判定
  if player.score > banker.score:
    print('プレイヤーの勝ちです．')
    result_key = 1
  elif player.score < banker.score:
    print('バンカーの勝ちです．')
    result_key = 2
  else:
    print('引き分けです．')
    result_key = 3

  # 結果に基づきお金を処理する
  moneys.result(result_key)
  input('精算します．(enter)')  # もうされてるけど
  clear_print_head(moneys,game_counter_add=False)  # カードを表示しない
  ## view(deck,player,banker,moneys,game_counter_add=False)  # カードを表示する

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
バカラを行う．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.2')
  parser.add_argument("-i", "--initial-tip", metavar="tip", type=float, default=10000, help="初期所持チップ")
  parser.add_argument("-d", "--check-draw", action="store_false", help="カードを引くときに確認しない")
  parser.add_argument("-p", "--players", metavar="名前", nargs='*', default=['あなた'], help="参加者の名前（何人でも）")
  parser.add_argument("-l", "--line-lengh", metavar="長さ", type=int, default=70, help="画面を区切る線（-）の長さ（個数）")
  parser.add_argument("-s", "--result-sort", action="store_true", help="最終結果を表示するときにソートする")
  options = parser.parse_args()

  global line_length
  line_length = options.line_lengh
  
  try:
    if not yn_inf('バカラを開始しますか？'):
      sys.exit()
  except (KeyboardInterrupt,BaseException):
    print('\nバカラを開始せず終了します．')
    sys.exit()

  moneys = Baccarat_Moneys()
  for player in options.players:
    moneys.append(Baccarat_Money(options.initial_tip,player))
 
  # バカラを無限に行う
  while True:
    try:
      baccarat(moneys.get_play_moneys(),options.check_draw)
      end_name_list = moneys.notip_end()
      if len(end_name_list):
        input('{}はベットすることができなくなったためゲームから除外されます．(enter)'.format('と'.join(end_name_list)))
      if not moneys.get_play_num():
        input('参加者がいなくなったためゲームを終了します．(enter)')
        break
      if not yn_inf('継続しますか？'):
        if yn_inf('本当に終了しますか？'):
          break
    except KeyboardInterrupt:
      try:
        input('\n中断されました．ベットされていたチップは返却されます．(enter)')
      except KeyboardInterrupt:
        pass
      for money in moneys:
        try:
          money.dividend(ratio=1,counter_add=False)
        except TypeError:
          pass
      break
  
  # 最終結果を表示
  if options.result_sort:
    moneys.sort_moneys()
  moneys.view(clear=True)

if(__name__ == '__main__'):
  main()
