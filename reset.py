#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xy.device import Device


def main():
  with Device() as device:
    device.reset()


if __name__ == '__main__':
  main()

