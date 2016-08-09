#!/usr/bin/env python
# coding=utf8
import dataset
import numpy as np

__author__ = 'tiantian'


def getDB(db_name):
    url = 'mysql:' + db_name
    db = dataset.connect(url)
    return db


def getTableName(db_name):
    db = getDB(db_name)
    tables = sorted(db.tables)
    return tables


def loadData(db_name, table_name):
    result = None
    db = getDB(db_name)
    db.begin()
    try:
        print table_name
        sql = 'select ts, ms, speed, max_c1, max_c2, max_c3 from `%s`' % str(table_name)
        print sql
        result = db.query(sql)
        # result = db[table_name].find()
        db.commit()
    except:
        db.rollback()
    x_ts = []
    x_ms = []
    y_max_c1 = []
    y_max_c2 = []
    y_max_c3 = []
    y_speed = []
    for mat in result:
        x_ts.append(mat['ts'])
        x_ms.append(mat['ms'])
        y_max_c1.append(mat['max_c1'])
        y_max_c2.append(mat['max_c2'])
        y_max_c3.append(mat['max_c3'])
        y_speed.append(mat['speed'])

    x = np.array(x_ts, float) + np.array(x_ms) / 1000.0
    array5 = np.zeros((len(x), 5))
    array5[:, 0] = x
    array5[:, 1] = y_max_c1
    array5[:, 2] = y_max_c2
    array5[:, 3] = y_max_c3
    array5[:, 4] = y_speed
    return array5


