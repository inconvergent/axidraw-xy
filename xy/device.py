# -*- coding: utf-8 -*-


from time import sleep
from time import time
import urllib.request
import json

HEADERS = {
    'Content-Type': 'application/json'
    }


class Device(object):

  def __init__(
      self,
      penup = 0,
      pendown = 1,
      host = 'http://localhost:4242',
      pen_delay = 0.0,
      verbose = False
      ):
    self._penup = penup
    self._pendown = pendown
    self._host = host
    self._url = host + '/v1/pen'
    self.pen_delay = pen_delay
    self.verbose = verbose

    self._moves = 0

    self.penup()

  def __enter__(self):
    input('enter to start ...')
    return self

  def __exit__(self,*arg, **args):
    self.penup()

  def _cmd(self, d):
    jsn = json.dumps(d)
    post = jsn.encode('utf-8')
    req = urllib.request.Request(self._url, data=post, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as res:
      # status = res.status
      # reason = res.reason
      a = json.loads(res.readall().decode('utf-8'))
      if self.verbose:
        x = a['x']
        y = a['y']
        last_duration = a['lastDuration']
        distance_counter = a['distanceCounter']
        print(x, y, last_duration, distance_counter)

  def move(self, x, y):
    if x>1.0 or x<0.0 or y>1.0 or y<0.0:
      raise ValueError('bad pen position.')

    self._moves += 1
    self._cmd({'x': x, 'y': y}
    )

  def pen(self, position):
    if position>1.0 or position<0.0:
      raise ValueError('bad pen elevation.')

    sleep(self.pen_delay)
    self._cmd({'state': position})
    sleep(self.pen_delay)

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

      self.move(*p[0,:], fast=True)
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

