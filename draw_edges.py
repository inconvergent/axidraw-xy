#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xy.device import Device

# from numpy import row_stack
# from numpy import min, max


def main(args):
  from modules.utils import get_edges_from_file as get

  fn = args.fn
  paths = get(fn)

  # ss = row_stack(paths)
  # print(min(ss[:,0], axis=0), max(ss[:,0], axis=0))
  # print(min(ss[:,1], axis=0), max(ss[:,1], axis=0))

  with Device(scale=0.99, penup=0.4) as device:
    device.do_paths(paths)


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

