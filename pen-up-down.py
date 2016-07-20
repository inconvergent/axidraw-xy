#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xy.device import Device


def main():
  with Device(verbose=True) as device:
    i = 1
    while True:
      if i % 2 == 0:
        print('down')
        device.pendown()
      else:
        print('up')
        device.penup()

      input('flip ...')

      i += 1


if __name__ == '__main__':
  main()

