#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xy.device import Device
from modules.utils import dots_to_circs


def main(args):
  from modules.utils import get_dots_from_file as get

  fn = args.fn
  rad = args.rad
  verts = get(fn)

  if rad is not None:
    if rad > 1.0 or rad < 0.001:
      print('ERROR: rad must be None or between 1.0 and 0.001.')
      exit(1)

  with Device(scale=0.99, penup=0.4) as device:
    if rad is not None:
      paths = dots_to_circs(verts, rad)
      device.do_paths(paths)
    else:
      device.do_dots(verts)

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--fn',
      type=str,
      required=True
      )
  parser.add_argument(
      '--rad',
      type=float,
      required=False,
      default=None
      )

  args = parser.parse_args()
  main(args)

