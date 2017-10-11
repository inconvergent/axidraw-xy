#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xy.device import Device

from numpy import row_stack


def main(args):
  from modules.utils import get_paths_from_file as get

  fn = args.fn
  paths = row_stack(get(fn, spatial_sort=False, spatial_concat=False))

  with Device(scale=0.99, drawing_speed=10, penup=1) as device:
    device.do_paths([paths])


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

