#!/usr/bin/env python
# coding=utf8
import os
import sys
import numpy as np
import datetime
from PySide.QtGui import *
from PySide.QtCore import *

os.environ["QT_API"] = "pyside"
import matplotlib

matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['xtick.minor.size'] = 3
matplotlib.rcParams['ytick.minor.size'] = 3
matplotlib.rcParams['axes.facecolor'] = 'none'

import seaborn as sns


class TimeWaveform(QDialog):
    def __init__(self, parent=None):
        super(TimeWaveform, self).__init__(parent)
        self.x = None
        self.y1 = None
        self.y2 = None
        self.y3 = None
        self.tx = None
        self.tem = []

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint | Qt.Dialog)
        self.setWindowTitle(u"电梯数据展示工具 ")
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self)
        self.splitterLayout = QHBoxLayout(self.splitter)
        self.treeView = QTreeView(self)
        self.model = QStandardItemModel(self)
        self.treeView.setModel(self.model)
        self.treeView.setHeaderHidden(True)

        fname = ['20160526.txt', '20160527.txt', '20160528.txt', '20160529.txt',
                 '20160530.txt', '20160531.txt', '20160601.txt', '20160602.txt',
                 '20160603.txt', '20160604.txt', '20160605.txt', '20160606.txt',
                 '20160607.txt', '20160608.txt', '20160609.txt', '20160610.txt',
                 '20160611.txt', '20160612.txt', '20160613.txt', '20160614.txt']
        fname = map(lambda s: (s.split('.'))[0], fname)
        for f in fname:
            ff = QStandardItem(f)
            ff.setToolTip(f)
            ff.setData({'datetime_data': f}, Qt.UserRole)
            self.model.appendRow(ff)

        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.splitterLayout.addWidget(self.treeView)
        self.treeView.header().setResizeMode(QHeaderView.ResizeToContents)

        self.frame = QWidget(self)
        self.frameLayout = QVBoxLayout(self.frame)
        self.splitterLayout.addWidget(self.frame)
        self.mainLayout.addWidget(self.splitter)
        self.splitter.setSizes([20, 400])
        self.figure = Figure(figsize=(400, 400), dpi=72, facecolor=('none'), edgecolor=('none'), frameon=False)
        self.figure.subplots_adjust(hspace=0.2)

        self.ax = self.figure.add_subplot(411)
        # self.ax.grid()
        # self.ax.minorticks_on()
        # self.ax.get_xaxis().set_visible(False)
        # self.ax.xaxis.grid(True, which='minor')
        self.ax2 = self.figure.add_subplot(412, sharex=self.ax, sharey=self.ax)
        # self.ax2.grid()
        # self.ax2.minorticks_on()
        # self.ax.get_xaxis().set_visible(False)
        # self.ax2.xaxis.grid(True, which='minor')
        # self.ax2.axes.get_xaxis().set_visible(False)
        self.ax3 = self.figure.add_subplot(413, sharex=self.ax, sharey=self.ax)
        # self.ax3.grid()
        # self.ax3.minorticks_on()
        # self.ax.get_xaxis().set_visible(False)
        # self.ax3.xaxis.grid(True, which='minor')
        # self.ax3.axes.get_xaxis().set_visible(True)

        self.ax4 = self.figure.add_subplot(414, sharex=self.ax)

        self.canvas = FigureCanvas(self.figure)
        self.treeView.doubleClicked.connect(self.showChart)
        self.toolBar = NavigationToolbar(self.canvas, self)
        self.frameLayout.addWidget(self.toolBar)
        self.frameLayout.addWidget(self.canvas)

    def showChart(self, s):
        tree_data = s.data(Qt.UserRole)
        array4 = np.loadtxt(tree_data['datetime_data'] + str('.txt'))
        t = array4[:, 0]
        self.x = map(lambda k: datetime.datetime.fromtimestamp(k), list(t))
        t1 = np.unique(np.asarray(t[::300], dtype=int))

        self.tx = map(lambda k: datetime.datetime.fromtimestamp(k), list(t1))

        self.y1 = array4[:, 1]/800.0
        self.y2 = array4[:, 2]/800.0
        self.y3 = array4[:, 3]/800.0

        print(len(self.tx))

        # self.tem = np.random.randint(20, 40, len(self.tx))
        for k in range(len(self.tx)):
            if self.tx[k].hour == 5:
                c7 = k
            elif self.tx[k].hour == 20:
                c20 = k
        print c7, c20
        self.tem = 10*np.sin(0.25*np.pi*t1 + 7.9*np.pi) + 30
        self.tem[:c7] = np.array([25]*c7)
        self.tem[c7:c20] = 0.8*np.sin(0.25*np.pi*t1[c7:c20] + 7.9*np.pi) + 38
        self.tem[c20:] = np.array([26]*len(self.tem[c20:]))

        self.ax.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        self.plotTrend()
        self.canvas.draw()

    def plotTrend(self):
        self.ax.plot(self.x, self.y1, label='max_c1', linestyle='solid', color='orange', linewidth=0.5)
        self.ax.set_title((str(self.x[0]))[:-3] + "~" + (str(self.x[-1]))[:-3] + "\n" + "speed at 2000RPM")
        self.ax.set_ylabel(u"Amplitude($m/s^2$)")
        self.ax.set_ylim(np.min([self.y1.min(), self.y2.min(), self.y3.min()]) - 1,
                                np.max([self.y1.max(), self.y2.max(), self.y3.max()]) + 3)
        self.ax.legend()

        self.ax2.plot(self.x, self.y2, label='max_c2', linestyle='solid', color='green', linewidth=0.5)
        self.ax2.set_ylabel(u"Amplitude($m/s^2$)")
        self.ax2.legend()

        self.ax3.plot(self.x, self.y3, label='max_c3', linestyle='solid', color='red', linewidth=0.5)
        self.ax3.set_ylabel(u"Amplitude($m/s^2$)")
        self.ax3.legend()

        self.ax4.plot(self.tx, self.tem, label='temperature', linestyle='solid', color='blue', linewidth=0.5)
        self.ax4.set_xlabel(u"Time($ms$)")
        self.ax4.set_ylabel(u"Temperature")
        self.ax4.legend()

        # self.ax.imshow([[0, 0], [1, 1]], cmap=plt.cm.Greys, alpha=0.15, extent=self.ax.axis(), aspect='auto')
        # self.ax2.imshow([[0, 0], [1, 1]], cmap=plt.cm.Greys, alpha=0.15, extent=self.ax2.axis(), aspect='auto')
        # self.ax3.imshow([[0, 0], [1, 1]], cmap=plt.cm.Greys, alpha=0.15, extent=self.ax3.axis(), aspect='auto')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = TimeWaveform()
    dialog.show()
    sys.exit(app.exec_())
