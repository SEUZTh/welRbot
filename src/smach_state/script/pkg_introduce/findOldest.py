#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy


def findOldest(age0, age1, age2):
    age_0 = int(age0)
    age_1 = int(age1)
    age_2 = int(age2)
    age = [age_0, age_1, age_2]
    return age.index(max(age))


if __name__ == '__main__':
    print findOldest('3', '4', '1')
