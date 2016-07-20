#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xy.device import Device


def main():

  from numpy import row_stack

  path = row_stack([[0.1, 0.1], [0.8, 0.1],  [0.8, 0.8], [0.1, 0.8], [0.1,0.1]])
  paths = [path]

  with Device(verbose=True) as device:
    device.do_paths(paths)


if __name__ == '__main__':
  main()

