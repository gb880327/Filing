#!python3
import sys
import time
import traceback
from ui.mainWindow import Ui_MainWindow
from ui.progress import Ui_Form
from PyQt5.QtCore import Qt
from PyQt5.Qt import (QThread, pyqtSlot, pyqtSignal, QTextCursor)
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QFile, QTextStream
from service.filing import Filing
import BreezeStyleSheets.breeze_resources


class MainWindow(QMainWindow):

    def __init__(self, win_ui):
        super(MainWindow, self).__init__()
        self.setFixedSize(669, 310)
        self.ui = win_ui
        win_ui.setupUi(self)
        self.progress = Progress(Ui_Form())
        self.ui.pushButton.clicked.connect(self.open_form)
        self.ui.toolButton.clicked.connect(lambda: self.openfile_namedialog(0))
        self.ui.toolButton_2.clicked.connect(lambda: self.openfile_namedialog(1))
        self.progress.signal.connect(self.over)
        self.ui.checkBox_2.setVisible(False)
        self.ui.checkBox.toggled.connect(self.toggled)

    def openfile_namedialog(self, index):
        file_dialog = QFileDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        path = file_dialog.getExistingDirectory(None, "Choose directory", "", options=options)
        if path:
            if index == 0:
                self.ui.lineEdit.setText(path)
            else:
                self.ui.lineEdit_2.setText(path)

    @pyqtSlot()
    def over(self):
        self.show()
        self.progress.hide()

    def open_form(self):
        o_path = self.ui.lineEdit.text()
        t_path = self.ui.lineEdit_2.text()
        if o_path is None or o_path == '':
            QMessageBox.warning(None, "操作提示！", "请选择源文件目录！", QMessageBox.Close, QMessageBox.Close)
            return
        if t_path is None or t_path == '':
            QMessageBox.warning(None, "操作提示！", "请选择目标文件目录！", QMessageBox.Close, QMessageBox.Close)
            return
        self.progress.open({
            'f_type': self.ui.comboBox.currentIndex(),
            'f_model': self.ui.comboBox_2.currentIndex(),
            'o_path': o_path,
            't_path': t_path,
            'hasCompress': self.ui.checkBox.isChecked(),
            'hasClear': self.ui.checkBox_2.isChecked()
        })
        self.hide()
        self.ui.checkBox.setChecked(False)
        self.ui.checkBox_2.setChecked(False)
        self.ui.checkBox_2.setVisible(False)
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()

    def toggled(self, checked):
        self.ui.checkBox_2.setVisible(checked)
        if not checked:
            self.ui.checkBox_2.setChecked(False)


class UpdateUI(QThread):
    signal = pyqtSignal(dict)
    params = {}

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def set_params(self, params: dict):
        self.params = params

    def run(self):
        try:
            filing = Filing(self.params)
            self.signal.emit({
                "num": 0,
                "msg": "=============开始文件整理================"
            })
            filing.get_file_list()
            file_list = filing.create_folder()
            total = len(file_list)

            for i, f in enumerate(file_list):
                filing.move_file(f['opath'], f['npath'])
                num = int(((i + 1) / total) * 100)
                num = num - 10 if num - 10 >= 0 else 0
                self.signal.emit({
                    "num": num,
                    "msg": "{0} 移动至 {1}".format(f['opath'], f['npath'])
                })
            if self.params['hasCompress']:
                self.signal.emit({
                    "num": 90,
                    "msg": "=============开始压缩文件============="
                })
                filing.compress_file(time.strftime("%Y%m%d", time.localtime()) + '.zip')
            self.signal.emit({
                "num": 100,
                "msg": "=============结束文件整理================"
            })
        except Exception as e:
            self.signal.emit({
                "num": -1,
                "msg": traceback.format_exc()
            })


class Progress(QWidget):
    signal = pyqtSignal()
    progress_num = 0

    def __init__(self, win_ui):
        super(Progress, self).__init__()
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui = win_ui
        win_ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.over)
        self.thread = UpdateUI()
        self.thread.signal.connect(self.callback)

    def close_window(self):
        if self.progress_num < 100:
            self.thread.wait()
            ret = QMessageBox.question(None, "操作提示！", "确认结束当前任务？", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if ret == QMessageBox.Yes:
                self.over()
        else:
            self.over()

    def open(self, params: dict):
        self.clear_ui()
        self.show()
        self.thread.set_params(params)
        self.thread.start()

    def over(self):
        self.signal.emit()

    def clear_ui(self):
        self.ui.pushButton.setProperty('enabled', False)
        self.ui.progressBar.setProperty('value', 0)
        cursor = self.ui.textBrowser.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.removeSelectedText()
        self.ui.textBrowser.setTextCursor(cursor)

    @pyqtSlot(dict)
    def callback(self, params: dict):
        self.ui.textBrowser.insertPlainText(params['msg'] + '\n')
        self.ui.textBrowser.moveCursor(QTextCursor.End)
        if 'num' in params.keys():
            self.ui.progressBar.setProperty('value', params['num'] if params['num'] >= 0 else 0)
            self.progress_num = params['num']
            if self.progress_num >= 100 or self.progress_num == -1:
                self.ui.pushButton.setProperty('enabled', True)
                self.thread.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    file = QFile("./BreezeStyleSheets/light.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    main = MainWindow(Ui_MainWindow())
    main.show()
    sys.exit(app.exec_())
