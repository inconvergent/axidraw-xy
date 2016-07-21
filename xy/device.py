# -*- coding: utf-8 -*-


from time import sleep
from time import time
import urllib.request
import json

HEADERS = {
    'Content-Type': 'application/json'
    }

# TODO: this is unlikely to work well for non-square drawings
# note that API accepts x/y positions in percentage of total plottable width/height
WIDTH = 12000.0
HEIGHT = 8720.0
ASPECT = HEIGHT/WIDTH

PEN_URL = '/v1/pen'
BOT_SETTINGS_URL = '/v1/settings/bot'


class Device(object):

  def __init__(
      self,
      penup = 0.5,
      pendown = 1,
      host = 'http://localhost:4242',
      pen_elevation_delay = 0.2,
      pen_delay = 0.0,
      drawing_speed = 7,
      moving_speed = 30,
      verbose = False
      ):
    self._penup = float(penup)
    self._pendown = float(pendown)
    self._host = host
    self._pen_url = host + PEN_URL
    self._bot_settings_url = host + BOT_SETTINGS_URL
    self._pen_elevation_delay = float(pen_elevation_delay)
    self._pen_delay = float(pen_delay)

    self._drawing_speed = int(drawing_speed)
    self._moving_speed = int(moving_speed)

    self.verbose = verbose

    self._settings()
    self.penup()

    self._moves = 0

  def __enter__(self):
    input('enter to start ...')
    return self

  def __exit__(self,*arg, **args):
    self.penup()
    self.move(0, 0)

  def _settings(self):
    self._cmd(
        {'speed:drawing': self._drawing_speed},
        self._bot_settings_url
        )
    self._cmd(
        {'speed:precision': 2},
        self._bot_settings_url
        )
    self._cmd(
        {'speed:min': 200},
        self._bot_settings_url
        )
    self._cmd(
        {'speed:max': 8000},
        self._bot_settings_url
        )
    self._cmd(
        {'speed:moving': self._moving_speed},
        self._bot_settings_url
        )

  def _cmd(self, d, url):
    jsn = json.dumps(d)
    post = jsn.encode('utf-8')
    req = urllib.request.Request(url, data=post, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as res:
      if res.status != 200:
        print('WARNING: error status ' + str(res.status) + ' ' + str(res.reason))
      a = json.loads(res.readall().decode('utf-8'))
      if self.verbose:
        print(json.dumps(a, sort_keys=True, indent=2))

  def move(self, x, y):
    if x>1.0 or x<0.0 or y>1.0 or y<0.0:
      raise ValueError('bad pen position.')

    self._moves += 1
    sleep(self._pen_delay)
    self._cmd(
        {'x': x*ASPECT*100.0, 'y': y*100.0},
        self._pen_url
        )

  def pen(self, position):
    if position>1.0 or position<0.0:
      raise ValueError('bad pen elevation.')

    sleep(self._pen_elevation_delay)
    self._cmd(
        {'state': position},
        self._pen_url
        )
    sleep(self._pen_elevation_delay)

  def penup(self):
    self.pen(self._penup)

  def pendown(self):
    self.pen(self._pendown)

  def _get_total_moves(self, paths):
    num = len(paths)-1
    for p in paths:
      num += len(p)-1
    return num

  # def do_dots(self, dots, info_leap=10):
  #
  #   t0 = time()
  #
  #   num = len(dots)
  #
  #   print('# dots: {:d}'.format(num))
  #
  #   self._moves = 0
  #   flip = 0
  #
  #   for i, p in enumerate(dots):
  #
  #     self.move(*p)
  #     self.pendown()
  #     self.penup()
  #     flip += 1
  #     if flip > info_leap:
  #       per = i/float(num)
  #       tot = (time()-t0)/3600.
  #       rem = tot/per - tot
  #       s = 'progress: {:d}/{:d} ({:3.03f}) run time: {:0.05f} hrs, remaining: {:0.05f} hrs'
  #       print(s.format(i, num, per, tot, rem))
  #       flip = 0
  #     flip += 1
  #
  #   self.penup()

  def do_paths(self, paths, info_leap=10):

    t0 = time()

    num = len(paths)
    moves = self._get_total_moves(paths)

    print('# paths: {:d}'.format(num))
    print('# moves: {:d}'.format(moves))

    self._moves = 0
    flip = 0

    for i, p in enumerate(paths):

      self.move(*p[0,:])
      self.pendown()
      flip += 1
      for xy in p[1:,:]:
        self.move(*xy)
        if flip > info_leap:
          per = self._moves/float(moves)
          tot = (time()-t0)/3600.
          rem = tot/per - tot
          s = 'progress: {:d}/{:d} ({:3.03f}) run time: {:0.05f} hrs, remaining: {:0.05f} hrs'
          print(s.format(self._moves, moves, per, tot, rem))
          flip = 0
        flip += 1

      self.penup()

    self.penup()

