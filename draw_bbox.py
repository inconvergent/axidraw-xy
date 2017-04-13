#!/usr/bin/python3
# -*- coding: utf-8 -*-


from xy.device import Device
from numpy import array


def main():

  paths = [array([
      [0, 0],
      [1, 0],
      [1, 1],
      [0, 1],
      [0, 0]], 'float')]

  with Device(scale=0.99, penup=0.4) as device:
    device.do_paths(paths)


if __name__ == '__main__':

  main()

