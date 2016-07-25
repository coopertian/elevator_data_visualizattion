#!/usr/bin/env python
# coding=utf8
from PySide.QtCore import *

__mDict = {}
__sigDict = {}
__mutex = QMutex()


class Notice(QObject):
    Sig = Signal(str)


def Clear():
    global __mDict
    global __mutex
    locker = QMutexLocker(__mutex)
    __mDict = {}
    __sigDict = {}


def __set(k, v):
    global __mDict
    global __mutex
    locker = QMutexLocker(__mutex)
    __mDict[k] = v


def Remove(k):
    global __mDict
    global __mutex
    locker = QMutexLocker(__mutex)
    if __mDict.has_key(k):
        __mDict.pop(k)


def Set(k, v):
    __set(k, v)
    if __sigDict.has_key(k):
        __sigDict[k].Sig.emit(k)


def Get(k, default=None):
    global __mDict
    global __mutex
    locker = QMutexLocker(__mutex)
    if __mDict.has_key(k):
        return __mDict[k]
    return default


def Has(k):
    global __mDict
    global __mutex
    locker = QMutexLocker(__mutex)
    return __mDict.has_key(k)


def Connect(k, receiver):
    global __mDict
    global __mutex
    global __sigDict
    locker = QMutexLocker(__mutex)
    if not __sigDict.has_key(k):
        __sigDict[k] = Notice()
    __sigDict[k].Sig.connect(receiver)

