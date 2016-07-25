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
    db = dataset.connect('mysql://root:pwd@127.0.0.1/cms_realtime')
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
    np.savetxt('20160614.txt', array4)


    # np.savetxt('timestamp_20160614.t
    # 'xt', x)
    # np.savetxt('y_max_c1_20160614.txt', np.array(y_max_c1))
    # np.savetxt('y_max_c2_20160614.txt', np.array(y_max_c2))
    # np.savetxt('y_max_c3_20160614.txt', np.array(y_max_c3))

    # x_datetime = map(lambda k: datetime.datetime.fromtimestamp(k), list(x))
    # return (x_datetime, y_max_c1, y_max_c2, y_max_c3)


def plotTrend(array4):
    x_datetime = array4[:, 0]
    x_datetime = map(lambda k: datetime.datetime.fromtimestamp(k), list(x_datetime))

    # dt = x_datetime[0]
    print x_datetime
    y_max_c1 = array4[:, 1]
    y_max_c2 = array4[:, 2]
    y_max_c3 = array4[:, 3]
    # x_dt = []
    # print x
    # for xi in x:]
    #     x_dt.append(datetime.datetime.strptime(xi, '%H:%M:%S:%f'))
    # x_datetime = x_dt
    # print x_datetime
    # hformat = dates.DateFormatter('%H:%M:%S.%f')

    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
    ax1.plot(x_datetime, y_max_c1, label='max_c1', linestyle='solid', color='blue', linewidth=0.5)

    ax1.legend()
    ax1.set_title(u"Time waveform at yake: " + str(x_datetime[0]) + "-" + str(x_datetime[-1]))
    ax2.plot(x_datetime, y_max_c2, label='max_c2', linestyle='solid', color='green', linewidth=0.5)
    ax2.legend()
    ax3.plot(x_datetime, y_max_c3, label='max_c3', linestyle='solid', color='red', linewidth=0.5)
    ax3.legend()
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    plt.show()


if __name__ == '__main__':
    # loadData()
    # x = np.loadtxt('timestamp.txt')
    # x_datetime = map(lambda k: datetime.datetime.fromtimestamp(k), list(x))
    # y_max_c1 = np.loadtxt('y_max_c1.txt')
    # y_max_c2 = np.loadtxt('y_max_c2.txt')
    # y_max_c3 = np.loadtxt('y_max_c3.txt')
    # plotTrend(x_datetime, y_max_c1, y_max_c2, y_max_c3)

    # array4 = np.loadtxt('20160526.txt')
    # plotTrend(array4)

    # f = open('times_yanji.txt')
    # time = eval(f.read())
    # # import matplotlib.pyplot as plt
    # # import numpy as np
    # # x = np.arange(len(time))
    # # plt.xticks(x, time)
    # y1 = np.loadtxt('max_c1_yanji.txt')
    # y2 = np.loadtxt('max_c2_yanji.txt')
    # y3 = np.loadtxt('max_c3_yanji.txt')
    # plotTrend(time, y1, y2, y3)

    filelist = ['20160527.txt',  '20160604.txt',
                '20160531.txt',  '20160608.txt',
                '20160528.txt', '20160529.txt',
                '20160602.txt', '20160613.txt',
                '20160601.txt', '20160607.txt',
                '20160614.txt', '20160612.txt',
                '20160611.txt', '20160605.txt',
                '20160606.txt', '20160526.txt',
                '20160610.txt', '20160530.txt',
                '20160603.txt', '20160609.txt']
    fname = []
    for f in sorted(filelist):
        print f
        fname.append(f)
    print fname






