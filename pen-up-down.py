#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xy.device import Device


PENUP = 0
PENDOWN = 1


def main():

  with Device() as device:

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

    input('\n\ndone ...')


if __name__ == '__main__':
  main()

