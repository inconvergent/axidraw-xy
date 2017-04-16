# -*- coding: utf-8 -*-


from time import sleep
from time import strftime
from numpy import array
from numpy import isclose
from numpy import row_stack
import urllib.request
import json

from modules.utils import print_values
from modules.utils import get_bounding_box

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
BUFFER_URL = '/v1/buffer'


class Device(object):

  def __init__(
      self,
      scale=1.0,
      penup=0.5,
      pendown=1,
      host='http://localhost:4242',
      drawing_speed=7,
      moving_speed=30,
      verbose=False
      ):
    self._scale = float(scale)
    self._penup = float(penup)
    self._pendown = float(pendown)
    self._host = host

    self._pen_url = host + PEN_URL
    self._bot_settings_url = host + BOT_SETTINGS_URL
    self._buffer_url = host + BUFFER_URL
    self._buffer_sleep = 5

    self._drawing_speed = int(drawing_speed)
    self._moving_speed = int(moving_speed) # TODO: this does not nothing atm?

    self.verbose = verbose

    self._settings()
    self.penup()

    self._moves = 0
    self._history = []

  def __enter__(self):
    input('enter to start ...')
    print('\nshowing progress on transferring data to the device buffer.\n')
    return self

  def __exit__(self, *arg, **args):
    self.penup()
    self.move(array([0, 0], 'float'))
    print_values(*get_bounding_box(row_stack(self._history)))
    self._show_buffer()

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

  def _show_buffer(self):
    print('now displaying buffer progress:')

    last = 0
    while True:
      buf = self._info(self._buffer_url)
      try:
        c = int(buf['count'])
      except Exception:
        c = 0

      if c <= 0:
        break
      print('{:s} buffer: {:d}, df: {:d}'.format(self._ts(), c, last-c))

      sleep(self._buffer_sleep)
      last = c

  def _ts(self):
    return strftime('%Y-%m-%d %H:%M:%S')

  def _cmd_del(self, url):
    req = urllib.request.Request(url, method='DELETE')
    with urllib.request.urlopen(req) as res:
      if res.status != 200:
        print('WARNING: error status ' + str(res.status) + ' ' + str(res.reason))
      # Convert from bytes to text
      resp_text = res.read().decode('UTF-8')
      # Use loads to decode from text
      a = json.loads(resp_text)
      if self.verbose:
        print(json.dumps(a, sort_keys=True, indent=2))

  def _cmd(self, d, url):
    jsn = json.dumps(d)
    post = jsn.encode('utf-8')
    req = urllib.request.Request(url, data=post, headers=HEADERS, method='PUT')
    with urllib.request.urlopen(req) as res:
      if res.status != 200:
        print('WARNING: error status ' + str(res.status) + ' ' + str(res.reason))
      # Convert from bytes to text
      resp_text = res.read().decode('UTF-8')
      # Use loads to decode from text
      a = json.loads(resp_text)
      if self.verbose:
        print(json.dumps(a, sort_keys=True, indent=2))

  def _info(self, url):
    req = urllib.request.Request(url, method='GET')
    with urllib.request.urlopen(req) as res:
      if res.status != 200:
        print('WARNING: error status ' + str(res.status) + ' ' + str(res.reason))
      # Convert from bytes to text
      resp_text = res.read().decode('UTF-8')
      # Use loads to decode from text
      a = json.loads(resp_text)
      return a
    return None

  def _xy_transform(self, xy):
    txy = xy*array([ASPECT, 1.0], 'float')*100.0*self._scale

    # TODO: this is a bit overzealous. consider improving.

    if any(txy > 100.0):
      print('WARNING: value greater than 100. correcting {:s}'.format(str(txy)))
      mask = isclose(txy, 100.0)
      txy[mask] = 100.0
      print('WARNING: corrected to {:s}'.format(str(txy)))
      if any(txy > 100.0):
        print('offending value:')
        print(txy)
        raise ValueError('unable to correct error. aborting.')

    if any(txy < 0.0):
      print('WARNING: value less than 0. correcting: {:s}'.format(str(txy)))
      mask = isclose(txy, 0.0)
      txy[mask] = 0.0
      print('WARNING: corrected to {:s}'.format(str(txy)))
      if any(txy < 0.0):
        print('offending value:')
        print(txy)
        raise ValueError('unable to correct error. aborting.')

    self._history.append(txy)
    return txy

  def reset(self):
    self._cmd_del(self._buffer_url)
    self.penup()
    self.move(array([0, 0], 'float'))

  def move(self, xy):
    self._moves += 1
    txy = self._xy_transform(xy)
    self._cmd(
        {'x': txy[0], 'y': txy[1]},
        self._pen_url
        )

  def pen(self, position):
    if position > 1.0 or position < 0.0:
      raise ValueError('bad pen elevation.')
    self._cmd(
        {'state': position},
        self._pen_url
        )

  def penup(self):
    self.pen(self._penup)

  def pendown(self):
    self.pen(self._pendown)

  def _get_total_moves(self, paths):
    num = len(paths)-1
    for p in paths:
      num += len(p)-1
    return num

  def do_paths(self, paths, info_leap=200):
    num = len(paths)
    moves = self._get_total_moves(paths)
    print('# paths: {:d}'.format(num))
    print('# moves: {:d}'.format(moves))
    self._moves = 0
    flip = 0

    for p in paths:
      self.move(p[0, :])
      self.pendown()
      flip += 1
      for xy in p[1:, :]:
        self.move(xy)
        if flip > info_leap:
          per = self._moves/float(moves)
          s = '{:s} progress: {:d}/{:d} ({:3.03f})'
          print(s.format(self._ts(), self._moves, moves, per))
          flip = 0
        flip += 1
      self.penup()

    self.penup()

  def do_dots(self, dots, info_leap=200):
    num = len(dots)
    moves = num
    print('# dots: {:d}'.format(num))
    print('# moves: {:d}'.format(moves))
    self._moves = 0
    flip = 0

    for xy in dots:
      self.move(xy)
      self.pendown()
      self.penup()
      flip += 2
      if flip > info_leap:
        per = self._moves/float(moves)
        s = '{:s} progress: {:d}/{:d} ({:3.03f})'
        print(s.format(self._ts(), self._moves, moves, per))
        flip = 0

    self.penup()

