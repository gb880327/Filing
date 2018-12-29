#!python3
import os
import time
import shutil
import zipfile
from PIL import Image


class Filing(object):

    def __init__(self, params: dict):
        self.filing_type = params['f_type']
        self.model = params['f_model']
        self.original_path = params['o_path']
        self.target_path = params['t_path']
        self.has_clear = params['hasClear']
        self.datelist = {}

    @staticmethod
    def timestamptotime(timestamp):
        timestruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d', timestruct)

    def get_filecreatetime(self, file_path):
        if self.filing_type == 0:
            ft = None
            if Filing.is_imagefile(file_path):
                ft = Filing.get_file_org_createtime(file_path)
            ft = ft if ft is not None else os.path.getctime(file_path)
        else:
            ft = os.path.getmtime(file_path)
        return ft[:10].replace(':', '-') if isinstance(ft, str) else self.timestamptotime(ft)

    @staticmethod
    def is_imagefile(file_path: str):
        suffix = file_path[file_path.rfind('.'):]
        return suffix.lower().strip() in ['.jpg', '.png', '.bmp', '.jpeg', '.gif']

    # 获取图片的原始创建时间
    @staticmethod
    def get_file_org_createtime(file_path):
        img = Image.open(file_path)
        info = img._getexif()
        return info[306] if info else None

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

    def compress_file(self, zip_file_name: str):
        filelist = []
        for root, dirs, files in os.walk(self.target_path):
            for name in files:
                filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(os.path.join(self.target_path, zip_file_name), 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
        for tar in filelist:
            arcname = tar[len(self.target_path):]
            zf.write(tar, arcname)
        zf.close()
        if self.has_clear:
            for root, dirs, files in os.walk(self.target_path):
                for f in dirs:
                    shutil.rmtree(os.path.join(root, f))
