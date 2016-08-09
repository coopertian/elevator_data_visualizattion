#!/usr/bin/env python
# coding=utf8

import os
import sys
import datetime

from PySide.QtGui import *
from PySide.QtCore import *
os.environ["QT_API"] = "pyside"
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['xtick.minor.size'] = 3
matplotlib.rcParams['ytick.minor.size'] = 3
matplotlib.rcParams['axes.facecolor'] = 'none'
import seaborn as sns
sns.set()

import database
import brake
import sharemem


class TimeWaveform(QDialog):
    def __init__(self, parent=None):
        super(TimeWaveform, self).__init__(parent)
        self.x = None
        self.y1 = None
        self.y2 = None
        self.y3 = None
        self.y4 = None
        self.showType = "realtime"
        self.showTypeBtn = None

        # added push button
        self.showTypeBtn = QPushButton(u"realtiime", self)
        self.showTypeBtn.setFlat(True)
        self.showTypeBtn.setStyleSheet('QPushButton {font: bold 20px;}')
        self.showTypeBtn.clicked.connect(self.showTypeBtnClicked)
        buttonWidget = QWidget(self)
        layout2 = QHBoxLayout(buttonWidget)
        layout2.setAlignment(Qt.AlignHCenter)
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.setSpacing(10)
        layout2.addWidget(self.showTypeBtn)
        layout = QVBoxLayout()
        layout.addWidget(buttonWidget)

        self.setWindowFlags(Qt.WindowCloseButtonHint |
                            Qt.WindowMinimizeButtonHint |
                            Qt.WindowMaximizeButtonHint |
                            Qt.Dialog)
        self.setWindowTitle(u"tool ")
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self)
        self.splitterLayout = QHBoxLayout(self.splitter)
        self.treeView = QTreeView(self)
        self.model = QStandardItemModel(self)
        self.treeView.setModel(self.model)
        self.treeView.setHeaderHidden(True)

        custom = ["yk001", "yk002", "yk003"]
        for cm in custom:
            custom = QStandardItem(cm)
            custom.setToolTip(cm)
            fnames = database.getTableName(cm)
            print "fnames == ", fnames
            for f in fnames:
                ff = QStandardItem(f)
                ff.setToolTip(f)
                custom.appendRow(ff)
                ff.setData({'custom_name': cm, 'datetime_data': f}, Qt.UserRole)
            self.model.appendRow(custom)

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

        self.ax = self.figure.add_subplot(412)

        self.ax2 = self.figure.add_subplot(413, sharex=self.ax, sharey=self.ax)

        self.ax3 = self.figure.add_subplot(414, sharex=self.ax, sharey=self.ax)

        self.ax4 = self.figure.add_subplot(411, sharex=self.ax)

        self.canvas = FigureCanvas(self.figure)
        self.treeView.doubleClicked.connect(self.showChart)
        self.toolBar = NavigationToolbar(self.canvas, self)
        self.frameLayout.addWidget(self.toolBar)
        self.frameLayout.addWidget(buttonWidget)
        self.frameLayout.addWidget(self.canvas)

        # load multi thread
        self.loadRealTimeThread = LoadRealTimeThread(waveform=self, parent=self)
        self.loadRealTimeThread.finished.connect(self.onFinished)

        self.loadBrakeAmplitudeThread = LoadBrakeAmplitudeThread(waveform=self, parent=self)
        self.loadBrakeAmplitudeThread.finished.connect(self.onFinished)

    def onFinished(self):
        self.ax.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        self.plots()
        self.canvas.draw()

    def showChart(self, s):
        self.showType = "realtime"
        self.showTypeBtn.setText(u"rl")
        data_tree = s.data(Qt.UserRole)
        if not data_tree:
            return
        sharemem.Set('data_tree', data_tree)
        self.loadRealTimeThread.start()
        self.showLoading()

    def plots(self):
        self.ax.plot(self.x, self.y1, label='max_c1', linestyle='solid', color='orange', linewidth=0.5)
        self.ax.set_ylabel(u"Amp")
        self.ax.set_ylim(np.min([self.y1.min(), self.y2.min(), self.y3.min()]) - 1,
                                np.max([self.y1.max(), self.y2.max(), self.y3.max()]) + 3)
        self.ax.legend()

        self.ax2.plot(self.x, self.y2, label='max_c2', linestyle='solid', color='green', linewidth=0.5)
        self.ax2.set_ylabel(u"Amp")
        self.ax2.legend()

        self.ax3.plot(self.x, self.y3, label='max_c3', linestyle='solid', color='red', linewidth=0.5)
        self.ax3.set_xlabel(u"Time")
        self.ax3.set_ylabel(u"Amp")
        self.ax3.legend()

        self.ax4.plot(self.x, self.y4, label='speed', linestyle='solid', color='blue', linewidth=0.5)
        self.ax4.set_title((str(self.x[0]))[:-3] + "~" + (str(self.x[-1]))[:-3])
        self.ax4.set_ylabel(u"Speed")
        self.ax4.legend()

    def onClicked(self):
        if self.showType == "realtime":
            self.loadRealTimeThread.start()
            self.showLoading()
        elif self.showType == "brake":
            self.loadBrakeAmplitudeThread.start()
            self.showLoading()

    def showTypeBtnClicked(self):
        if self.showType == "realtime":
            self.showType = "brake"
            self.showTypeBtn.setText(u"br")
            self.onClicked()
        elif self.showType == "brake":
            self.showType = "realtime"
            self.showTypeBtn.setText(u"rl")
            self.onClicked()

    def showLoading(self):
        self.ax.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        self.ax4.set_title("Loading...")
        self.canvas.update()


# thread: load data from database
class LoadRealTimeThread(QThread):
    def __init__(self, waveform=None, parent=None):
        super(LoadRealTimeThread, self).__init__(parent)
        self.waveForm = waveform

    def run(self, *args, **kwargs):
        data_tree = sharemem.Get('data_tree')
        db_name = data_tree['custom_name']
        table_name = data_tree['datetime_data']
        data_matrix = database.loadData(db_name, table_name)
        self.waveForm.x = map(lambda k: datetime.datetime.fromtimestamp(k), list(data_matrix[:, 0]))
        self.waveForm.y1 = data_matrix[:, 1]
        self.waveForm.y2 = data_matrix[:, 2]
        self.waveForm.y3 = data_matrix[:, 3]
        self.waveForm.y4 = data_matrix[:, 4]


# thread: find brake from real time dataset
class LoadBrakeAmplitudeThread(QThread):
    def __init__(self, waveform=None, parent=None):
        super(LoadBrakeAmplitudeThread, self).__init__(parent)
        self.waveForm = waveform

    def run(self, *args, **kwargs):
        data_tree = sharemem.Get('data_tree')
        db_name = data_tree['custom_name']
        table_name = data_tree['datetime_data']
        data_matrix = database.loadData(db_name, table_name)

        idx_brake = brake.getIdx(data_matrix[:, 4], data_matrix[:, 3])
        self.waveForm.x = map(lambda k: datetime.datetime.fromtimestamp(k), list(data_matrix[idx_brake, 0]))
        self.waveForm.y1 = data_matrix[idx_brake, 1]
        self.waveForm.y2 = data_matrix[idx_brake, 2]
        self.waveForm.y3 = data_matrix[idx_brake, 3]
        self.waveForm.y4 = data_matrix[idx_brake, 4]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = TimeWaveform()
    dialog.show()
    sys.exit(app.exec_())
