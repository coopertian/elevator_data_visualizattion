#!/usr/bin/env python
# coding=utf8

import numpy as np
from scipy import signal

from utils import threads

__author__ = 'tiantian'


@threads(5)
def find_brake(speed, y_c):
    if sum(speed)/len(speed) == 0:
        speed = y_c
    temp = speed
    # added noise
    temp += np.random.random()

    peakind = signal.find_peaks_cwt(temp, np.arange(1, 10), max_distances=np.arange(1, 10)**2)
    peakind = list(np.array(peakind) - 1)
    # return peakind
    brake = []
    for k in range(1, len(peakind)):
        ka = peakind[k-1]
        kb = peakind[k]
        if ka+1 < kb:
            max_idx = (y_c[ka+1:kb]).argmax()
        elif ka+1 == kb:
            max_idx = ka + 1
        else:
            print("Could not find extrema.")
        brake.append(ka + max_idx)
    return brake


def getIdx(speed, yc, n=5):
    block = len(speed)/n
    temp1 = (speed[:block*n]).reshape((n, block))
    temp2 = (yc[:block*n]).reshape((n, block))
    if n*block == len(speed):
        speed_list = list(temp1)
        yc_list = list(temp2)
    elif n*block < len(speed):
        speed_list = list(temp1)
        speed_list[-1] = np.array(list(speed_list[-1]) +
                                  list(speed[n*block:]))
        yc_list = list(temp2)
        yc_list[-1] = np.array(list(yc_list[-1]) +
                                  list(yc[n*block:]))
    responses = [find_brake(speed_list[i], yc_list[i]) for i in range(len(speed_list))]

    idx = [response.result for response in responses]
    idx_brake = []
    for i in idx:
        idx_brake += i
    return sorted(idx_brake)




