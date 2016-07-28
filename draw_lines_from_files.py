#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xy.device import Device


def main(args):
  from modules.utils import get_paths_from_n_files as get

  pattern = args.pattern
  steps = args.steps
  stride = args.stride
  skip = args.skip

  paths = get(pattern, skip, steps, stride, spatial_concat=True, spatial_concat_eps=1e-4)

  with Device(scale=0.99, penup=0.4) as device:
    device.do_paths(paths)


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--pattern',
    type=str,
    required=True
  )
  parser.add_argument(
    '--steps',
    type=int,
    default=100000
  )
  parser.add_argument(
    '--stride',
    type=int,
    default=1
  )
  parser.add_argument(
    '--skip',
    type=int,
    default=0
  )

  args = parser.parse_args()
  main(args)

