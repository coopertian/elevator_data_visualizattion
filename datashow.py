#!/usr/bin/env python
# coding=utf-8
import dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime

__author__ = 'tiantian'


def loadData():
    result = None
    db = dataset.connect('mysql:')
    db.begin()
    try:
        sql = 'select ts, ms, max_c1, max_c2, max_c3 from `20160614` ;'
        result = db.query(sql)
        db.commit()
    except:
        db.rollback()

    x_ts = []
    x_ms = []
    y_max_c1 = []
    y_max_c2 = []
    y_max_c3 = []
    for mat in result:
        x_ts.append(mat['ts'])
        x_ms.append(mat['ms'])
        y_max_c1.append(mat['max_c1'])
        y_max_c2.append(mat['max_c2'])
        y_max_c3.append(mat['max_c3'])

    x = np.array(x_ts, float) + np.array(x_ms) / 1000.0
    array4 = np.zeros((len(x), 4))
    array4[:, 0] = x
    array4[:, 1] = y_max_c1
    array4[:, 2] = y_max_c2
    array4[:, 3] = y_max_c3


def plotTrend(array4):
    x_datetime = array4[:, 0]
    x_datetime = map(lambda k: datetime.datetime.fromtimestamp(k), list(x_datetime))

    # dt = x_datetime[0]
    print x_datetime
    y_max_c1 = array4[:, 1]
    y_max_c2 = array4[:, 2]
    y_max_c3 = array4[:, 3]

    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
    ax1.plot(x_datetime, y_max_c1, label='max_c1', linestyle='solid', color='blue', linewidth=0.5)

    ax1.legend()
    ax1.set_title(u"Time waveform: " + str(x_datetime[0]) + "-" + str(x_datetime[-1]))
    ax2.plot(x_datetime, y_max_c2, label='max_c2', linestyle='solid', color='green', linewidth=0.5)
    ax2.legend()
    ax3.plot(x_datetime, y_max_c3, label='max_c3', linestyle='solid', color='red', linewidth=0.5)
    ax3.legend()
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    plt.show()






