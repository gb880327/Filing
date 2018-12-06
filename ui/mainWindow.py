# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(669, 260)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 59, 16))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(110, 20, 171, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 30, 59, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(440, 20, 161, 41))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 80, 81, 31))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 80, 441, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(560, 80, 81, 31))
        self.toolButton.setObjectName("toolButton")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 91, 31))
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 140, 441, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setGeometry(QtCore.QRect(560, 140, 81, 31))
        self.toolButton_2.setObjectName("toolButton_2")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 200, 621, 51))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 669, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "文件归档工具"))
        self.label.setText(_translate("MainWindow", "分类规则："))
        self.comboBox.setItemText(0, _translate("MainWindow", "创建时间"))
        self.comboBox.setItemText(1, _translate("MainWindow", "修改时间"))
        self.label_2.setText(_translate("MainWindow", "分类方式："))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "移动文件"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "复制文件"))
        self.label_3.setText(_translate("MainWindow", "源文件目录："))
        self.toolButton.setText(_translate("MainWindow", "请选择..."))
        self.toolButton.clicked.connect(lambda: self.openfileNameDialog(0))
        self.label_4.setText(_translate("MainWindow", "目标文件目录："))
        self.toolButton_2.setText(_translate("MainWindow", "请选择..."))
        self.toolButton_2.clicked.connect(lambda: self.openfileNameDialog(1))
        self.pushButton.setText(_translate("MainWindow", "开始"))

    def openfileNameDialog(self, index):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        options |= QtWidgets.QFileDialog.ShowDirsOnly
        path = QtWidgets.QFileDialog.getExistingDirectory(None, "Choose directory", "", options=options)
        if path:
            if index == 0:
                self.lineEdit.setText(path)
            else:
                self.lineEdit_2.setText(path)

    def start(self, main: QtWidgets.QWidget, form: QtWidgets.QWidget):
        f_type = self.comboBox.currentIndex()
        f_model = self.comboBox_2.currentIndex()
        o_path = self.lineEdit.text()
        t_path = self.lineEdit_2.text()
        if o_path is None or o_path == '':
            msgBox = QtWidgets.QMessageBox.warning(None, "操作提示！", "请选择源文件目录！", QtWidgets.QMessageBox.Close,
                                                   QtWidgets.QMessageBox.Close)
            return
        if t_path is None or t_path == '':
            QtWidgets.QMessageBox.warning(None, "操作提示！", "请选择目标文件目录！", QtWidgets.QMessageBox.Close,
                                          QtWidgets.QMessageBox.Close)
            return
        form.show()
        main.hide()
