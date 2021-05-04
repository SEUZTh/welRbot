#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys


def save_info(name, age, favoriteDrink, pos):
    fo = open(
        "./welRobot_ws/src/smach_state/script/pkg_save_info/info/guests_info.txt",
        "a+")
    info = "%s, %s, %s, %s; \n" % (str(name), str(age), str(favoriteDrink),
                                   str(pos))
    fo.write(info)
    fo.close()


if __name__ == '__main__':
    save_info('Mike', 21, 'cola', [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0, 7.0)])
