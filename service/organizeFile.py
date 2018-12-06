#!python3

import optparse
import os
import sys
import time
import shutil


class OrganizeFile:

    def __init__(self, path, time_mode, fname):
        self.dirpath = path if path is not None else './'
        self.time_model = time_mode if time_mode is not None else 'c'
        self.filename = fname

    @staticmethod
    def timestamptotime(timestamp):
        timestruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d', timestruct)

    def get_filecreatetime(self, file_path):
        file_path = str(file_path, 'utf-8')
        ft = os.path.getctime(file_path) if self.time_model == 'c' else os.path.getmtime(file_path)
        return self.timestamptotime(ft)

    def start(self):
        print("=============开始分析文件================")
        filelist = os.listdir(self.dirpath)
        datelist = {}
        for f in filelist:
            realpath = os.path.join(self.dirpath, f)
            if f == self.filename or f.startswith('.') or not os.path.isfile(realpath):
                continue
            file_time = self.get_filecreatetime(realpath)
            if file_time not in datelist.keys():
                datelist[file_time] = []
            datelist[file_time].append(realpath)

        print("=============结束分析文件================")
        print("=============开始文件归类================")
        for t in datelist.keys():
            newpath = os.path.join(self.dirpath, t)
            if not os.path.exists(newpath):
                os.mkdir(newpath)
            for f in datelist[t]:
                shutil.move(f, newpath)
        print("=============结束文件归类================")


if __name__ == '__main__':
    # parser = optparse.OptionParser('usage %prog -p <file path> -t <time mode  c-create,m->modif')
    # parser.add_option('-p', dest='path', type='string', help='File dir path')
    # parser.add_option('-t', dest='time', type='string', help='Time model c-create,m-modification')
    # (options, args) = parser.parse_args()
    # timemodel = options.time
    # dirpath = options.path

    # dirpath = os.path.dirname(os.path.realpath(sys.executable))

    value = input("请选择归类方式：\n1、创建时间\n2、修改时间\n请选择：")
    while int(value) != 1 and int(value) != 2:
        print("输入参数错误！请重新输入")
        value = input("请选择归类方式：\n1、创建时间\n2、修改时间\n请选择：")
    timemodel = 'c' if int(value) == 1 else 'm'
    dirpath = os.path.abspath(sys.argv[0])
    filename = dirpath[dirpath.rfind('/')+1:]
    dirpath = dirpath[:dirpath.rfind('/')]
    organize = OrganizeFile(dirpath, timemodel, filename)
    # organize.start()
