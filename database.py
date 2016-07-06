#!/usr/bin/env python
# coding=utf8
import dataset
import numpy as np

__author__ = 'tiantian'


def getTableName():
    db = dataset.connect('mysql://root:pwd@127.0.0.1/cms_realtime')
    tables = sorted(db.tables)
    return tables


def loadData(table_name):
    result = None
    db = dataset.connect('mysql://root:pwd@127.0.0.1/cms_realtime')
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

#
# if __name__ == '__main__':
#     table_name = '20160706'
#     array5 = loadData(table_name)
#     print array5