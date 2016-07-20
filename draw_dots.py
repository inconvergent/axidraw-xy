#!/usr/bin/python
# -*- coding: utf-8 -*-



from xy.device import Device


PENUP = 130
PENDOWN = 160

SMAX = 150
TTY = '/dev/ttyUSB0'



def main(args):

  from modules.utils import get_dots_from_file as get

  fn = args.fn

  dots = get(fn, SMAX)

  with Device(
    TTY,
    penup=PENUP,
    pendown=PENDOWN,
    verbose=False,
    min_delay=350,
    max_delay=350
  ) as device:

    device.do_dots(dots)


if __name__ == '__main__':

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--fn',
    type=str,
    required=True
  )

  args = parser.parse_args()
  main(args)

