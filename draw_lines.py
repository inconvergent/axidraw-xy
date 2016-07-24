#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xy.device import Device


def main(args):
  from modules.utils import get_paths_from_file as get

  fn = args.fn
  paths = get(fn, 0.99, spatial_concat=True, spatial_concat_eps=1e-4)

  with Device(penup=0.4) as device:
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

