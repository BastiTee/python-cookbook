# -*- coding: utf-8 -*-
"""Minimal game of knight implementation."""

from random import randint


def __run_pass(knights):
    print(knights)
    if len(knights) == 1:
        return
    knights[1] = (knights[1][0] - knights[0][1], knights[1][1], knights[1][2])
    __run_pass([k for k in knights[1:] + [knights[0]] if k[0] > 0])


if __name__ == '__main__':
    __run_pass([(randint(10, 30), randint(5, 10), r) for r in range(5)])
