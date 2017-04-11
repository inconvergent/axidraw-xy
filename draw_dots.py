#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xy.device import Device


def main(args):
  from modules.utils import get_dots_from_file as get

  fn = args.fn
  verts = get(fn)

  print(verts)

  with Device(scale=0.99, penup=0.4) as device:
    device.do_dots(verts)


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

