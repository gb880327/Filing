#!python3
import os
import time
import shutil


class Filing(object):

    def __init__(self, params: dict):
        self.filing_type = params['f_type']
        self.model = params['f_model']
        self.original_path = params['o_path']
        self.target_path = params['t_path']
        self.datelist = {}

    @staticmethod
    def timestamptotime(timestamp):
        timestruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d', timestruct)

    def get_filecreatetime(self, file_path):
        ft = os.path.getctime(file_path) if self.filing_type == 0 else os.path.getmtime(file_path)
        return self.timestamptotime(ft)

    def get_file_list(self):
        filelist = os.listdir(self.original_path)
        for f in filelist:
            realpath = os.path.join(self.original_path, f)
            if f.startswith('.') or not os.path.isfile(realpath):
                continue
            file_time = self.get_filecreatetime(realpath)
            if file_time not in self.datelist.keys():
                self.datelist[file_time] = []
            self.datelist[file_time].append(realpath)

    def create_folder(self):
        file_list = []
        for t in self.datelist.keys():
            newpath = os.path.join(self.target_path, t)
            if not os.path.exists(newpath):
                os.mkdir(newpath)
            for f in self.datelist[t]:
                file_list.append({
                    'opath': f,
                    'npath': newpath
                })
        return file_list

    def move_file(self, opath, newpath):
        if self.model == 0:
            shutil.move(opath, newpath)
        else:
            shutil.copy(opath, newpath)
